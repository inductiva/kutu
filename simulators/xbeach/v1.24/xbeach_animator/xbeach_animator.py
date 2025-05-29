import os
import shutil
import argparse
import pathlib
import sys
from data_processing import open_netcdf_file
from visualization import animate_wave, export_vtk_sequence
from xbTools.xbeachpost import XBeachModelAnalysis as BaseXBeachModelAnalysis

GLOBAL_VARS_PARAM_NAME = "globalvar"
REQUIRED_VARS_FOR_ANIMATION = {'zb', 'zs', 'H'}
OUTPUT_FORMAT_PARAM_NAME = "outputformat"
OUTPUT_FILENAME_PARAM_NAME = "ncfilename"
DEFAULT_OUTPUT_FILENAME = "xboutput.nc"
DEFAULT_OUTPUT_FORMAT = "netcdf"


class PatchedXBeachModelAnalysis(BaseXBeachModelAnalysis):

    def get_metadata(self):
        path = pathlib.Path(self.model_path) / "XBlog.txt"
        if not path.exists():
            raise FileNotFoundError(f"XBlog.txt not found at {path}")
        with open(path, "r") as f:
            self.metadata = {
                line.split('=')[0].strip(): line.split('=')[1].strip()
                for line in f
                if '=' in line and 'Finished' not in line
            }


def fetch_simulation_by_task_id(task_id: str,
                                overwrite: bool = False) -> pathlib.Path:
    """
    """
    import inductiva
    task = inductiva.tasks.Task(task_id)
    base_output = pathlib.Path(inductiva.get_output_dir()) / task_id

    # If already present and user didn't ask to overwrite, just return it
    if base_output.exists() and not overwrite:
        return base_output

    output_dir = pathlib.Path(inductiva.get_output_dir()) / task_id

    task.download_outputs()
    task.download_inputs()

    return output_dir


def _make_combined_dir(source_dirs: list[pathlib.Path],
                       combined_dir: pathlib.Path) -> pathlib.Path:
    """
    Create (or recreate) `combined_dir` and symlink every entry from each
    path in `source_dirs` into it. If two source dirs contain the same
    filename, the second is silently ignored.
    """
    if combined_dir.exists():
        shutil.rmtree(combined_dir)
    combined_dir.mkdir()

    for src_dir in source_dirs:
        if not src_dir.is_dir():
            raise FileNotFoundError(
                f"Expected a directory at {src_dir}, got nothing")
        for item in src_dir.iterdir():
            dest = combined_dir / item.name
            if dest.exists():
                # skip duplicates
                continue
            os.symlink(item.resolve(), dest)

    return combined_dir


def merge_separate_dirs(
    input_dir: pathlib.Path,
    outputs_dir: pathlib.Path,
    combined_name: str = ".xbeach_combined",
) -> pathlib.Path:
    """
    Take two flat dirs—one with all inputs, one with all outputs—and
    merge them into a symlink tree named `combined_name` alongside the inputs.
    """
    combined_dir = input_dir.parent / combined_name
    return _make_combined_dir([input_dir, outputs_dir], combined_dir)


def merge_simulation_dirs(
        results_dir: pathlib.Path,
        combined_name: str = ".xbeach_combined") -> pathlib.Path:
    """
    Inside `results_dir`, find `inputs/<sim_subdir>/` and `outputs/`,
    then merge both into a symlink tree named `combined_name` under results_dir.
    """
    results_dir = pathlib.Path(results_dir)
    inputs_root = results_dir / "inputs"
    if not inputs_root.is_dir():
        raise FileNotFoundError(f"No 'inputs' folder found in {results_dir!r}")

    sim_subdirs = [p for p in inputs_root.iterdir() if p.is_dir()]
    if not sim_subdirs:
        raise FileNotFoundError(f"No subdirectory inside {inputs_root!r}")
    sim_input_dir = sim_subdirs[0]

    outputs_root = results_dir / "outputs"
    if not outputs_root.is_dir():
        raise FileNotFoundError(f"No 'outputs' folder found in {results_dir!r}")

    combined_dir = results_dir / combined_name
    return _make_combined_dir([sim_input_dir, outputs_root], combined_dir)


def _verify_xbeach_simulation_minimal_requirements(
    sim_data: PatchedXBeachModelAnalysis,) -> tuple[bool, str]:

    # Check for correct global variables
    global_vars: set[str] = set(sim_data.params.get(GLOBAL_VARS_PARAM_NAME, []))

    if not global_vars or not REQUIRED_VARS_FOR_ANIMATION.issubset(global_vars):
        return (False,
                "Global variables zb, zs, and H not found in the output file.")

    # Check for correct output format
    output_format = sim_data.metadata.get(OUTPUT_FORMAT_PARAM_NAME, "")
    if output_format != DEFAULT_OUTPUT_FORMAT:
        return False, (f"Output format {output_format} is not supported. "
                       f"Only netcdf is supported.")

    # Check for correct output file name
    output_filename = DEFAULT_OUTPUT_FILENAME
    if sim_data.metadata.get(OUTPUT_FILENAME_PARAM_NAME,
                             "None specified") != "None specified":
        output_filename = sim_data.metadata[OUTPUT_FILENAME_PARAM_NAME]

    return True, output_filename


def parse_args():
    p = argparse.ArgumentParser(
        description=
        "Visualize or export VTK meshes from an XBeach netCDF simulation.")

    src_group = p.add_mutually_exclusive_group(required=True)
    src_group.add_argument(
        "--results-dir",
        type=pathlib.Path,
        help=
        "Path to an XBeach results dir (must contain inputs/ and outputs/).",
    )
    src_group.add_argument(
        "--task-id",
        type=str,
        help="Task ID for a simulation (will download inputs/outputs).",
    )
    src_group.add_argument(
        "--input-dir",
        type=pathlib.Path,
        help="Path to the inputs directory (when outputs are elsewhere).",
    )

    # Only meaningful when --input-dir is chosen:
    p.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="Path to the outputs directory (used with --input-dir).",
    )

    p.add_argument(
        "--overwrite-downloads",
        action="store_true",
        help=
        "If set, always re-download inputs/outputs even if they already exist.")

    p.add_argument(
        "--animate-wave",
        action="store_true",
        help="Generate a PyVista animation (default fps=10, angle=30,-135).")

    p.add_argument("--export-vtk",
                   action="store_true",
                   help="Export seabed + wave time-series as VTK files.")

    p.add_argument(
        "--fps",
        type=int,
        default=10,
        help="Frames per second for the animation (if --animate-wave).")

    p.add_argument(
        "--angle",
        type=float,
        nargs=2,
        metavar=("ELEV", "AZIM"),
        default=(30.0, -45.0),
        help="Camera elevation and azimuth in degrees for the animation.")

    p.add_argument(
        "--vtk-dir",
        type=pathlib.Path,
        default=pathlib.Path("VTK"),
        help="Directory in which to write VTK files (if --export-vtk).")

    p.add_argument(
        "--vertical-fraction",
        type=float,
        default=0.2,
        help="Vertical-exaggeration fraction for both animation and VTK export."
    )

    return p.parse_args()


def main():
    args = parse_args()

    if not args.animate_wave and not args.export_vtk:
        print(
            "Error: you must specify at least one of --animate-wave or "
            "--export-vtk\n",
            file=sys.stderr)
        sys.exit(1)

    # Decide source of inputs/outputs and build `combined` symlink folder
    if args.input_dir:
        if not args.output_dir:
            print("Error: --input-dir requires --output-dir", file=sys.stderr)
            sys.exit(1)
        combined = merge_separate_dirs(args.input_dir, args.output_dir)

    elif args.results_dir:
        if not args.results_dir.is_dir():
            print(f"Error: {args.results_dir!r} is not a directory.",
                  file=sys.stderr)
            sys.exit(1)
        combined = merge_simulation_dirs(args.results_dir)

    else:
        # must be a task_id
        results_dir = fetch_simulation_by_task_id(args.task_id,
                                                  args.overwrite_downloads)
        if not results_dir.is_dir():
            print(f"Error: {results_dir!r} is not a directory.",
                  file=sys.stderr)
            sys.exit(1)
        combined = merge_simulation_dirs(results_dir)

    # Load and verify simulation
    sim = PatchedXBeachModelAnalysis("CLI_Run", str(combined))
    ok, nc_filename_or_err = _verify_xbeach_simulation_minimal_requirements(sim)
    if not ok:
        print(f"Error: {nc_filename_or_err}", file=sys.stderr)
        sys.exit(1)

    nc_path = combined / nc_filename_or_err
    if not nc_path.exists():
        print(f"Error: NetCDF file {nc_path!r} does not exist.",
              file=sys.stderr)
        sys.exit(1)

    dataset = open_netcdf_file(str(nc_path))

    if args.animate_wave:
        print("▶ Generating animation…")
        animate_wave(dataset,
                     out_file="wave.mp4",
                     angle=tuple(args.angle),
                     fps=args.fps)
        print("✔ Animation done.")

    if args.export_vtk:
        print("▶ Exporting VTK sequence…")
        export_vtk_sequence(dataset,
                            vtk_dir=str(args.vtk_dir),
                            target_vertical_fraction=args.vertical_fraction)
        print("✔ VTK export done.")


if __name__ == "__main__":
    main()

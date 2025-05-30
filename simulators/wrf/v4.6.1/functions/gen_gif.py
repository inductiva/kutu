import os
import argparse
from netCDF4 import Dataset
from wrf import getvar, to_np, get_cartopy, latlon_coords
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
import imageio
import numpy as np
import cartopy.config as cfg


cfg['data_dir'] = '/root/.local/share/cartopy'

def process_files(wrf_files, output_dir, var="RAINNC", fps=3):
    if not wrf_files:
        print("No WRF output files found.")
        return

    # Create a folder to store the frames
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    frame_paths = []

    # Find global max and min var value for color scale
    min_var = np.inf
    max_var = -np.inf
    for file in wrf_files:
        try:
            ncfile = Dataset(file)
            var_data = to_np(getvar(ncfile, var))
            max_var = max(max_var, var_data.max())
            min_var = min(min_var, var_data.min())
        except Exception as e:
            print(f"Warning: Skipping {file} due to error: {e}")
            continue

    # Generate plots
    for i, file in enumerate(wrf_files):
        print(f"Processing: {file}")
        ncfile = Dataset(file)

        try:
            measure_var = getvar(ncfile, var)

        except Exception as e:
            print(f"Failed to extract {var} for {file}: {e}")
            continue

        lats, lons = latlon_coords(measure_var)

        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=get_cartopy(measure_var))
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        levels = np.linspace(min_var, max_var, 100)  # 100 levels, adjust as needed
        contour = plt.contourf(to_np(lons),
                               to_np(lats),
                               to_np(measure_var),
                               levels=levels,
                               cmap="Blues",
                               vmin=min_var,
                               vmax=max_var,
                               transform=crs.PlateCarree())
        
        cbar = plt.colorbar(contour, ax=ax, orientation="vertical", pad=0.02)
        cbar.set_label(f"{var}")
        plt.title(f"{var} {os.path.basename(file)}")

        frame_file = os.path.join(frames_dir, f"frame_{i:03d}.png")
        plt.savefig(frame_file, bbox_inches="tight")
        frame_paths.append(frame_file)
        plt.close()

    # Generate GIF
    gif_filename = os.path.join(output_dir, f"{var}_animation.gif")
    imageio.mimsave(gif_filename, [imageio.imread(f) for f in frame_paths], fps=fps)
    print(f"\nGIF saved as: {gif_filename}")


def main():
    parser = argparse.ArgumentParser(description="Generate animation from WRF output files.")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="List of WRF output files to process (e.g., wrfout_d01_2020-01-01_00_00_00 ...)"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save output frames and animation (default: current directory)"
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=3,
        help="Frames per second for the output GIF (default: 3)"
    )


    parser.add_argument(
        "--var",
        default="RAINNC",
        help="Variable to visualize (default: RAINNC)"
    )

    args = parser.parse_args()
    wrf_files = [f for f in args.files if os.path.isfile(f)]

    if not wrf_files:
        print("Error: No valid files were found in the list.")
        return

    process_files(wrf_files, args.output_dir, var=args.var, fps=args.fps)


if __name__ == "__main__":
    main()

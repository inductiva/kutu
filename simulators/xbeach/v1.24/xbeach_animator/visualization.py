import math
import pathlib
from typing import Iterator, NamedTuple
import numpy as np
import pyvista as pv
from data_processing import get_simulation_variables


class PointCloudData(NamedTuple):
    bed_points: np.ndarray
    wave_points: np.ndarray
    grid_dimensions: tuple[int, int, int]
    min_z: float
    vertical_exaggeration: float
    center_x: float
    center_y: float


def _build_structured_grid(points: np.ndarray, dims: tuple[int, int, int],
                           name: str) -> pv.StructuredGrid:
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = dims
    grid[name] = points[:, 2]
    return grid


def prepare_point_clouds(
        x_grid: np.ndarray,
        y_grid: np.ndarray,
        bed_elevation: np.ndarray,
        seabed_clipped: np.ndarray,
        wave_height_initial: np.ndarray,
        target_vertical_fraction: float = 0.2) -> PointCloudData:
    """
    Prepare recentered and vertically exaggerated point clouds for seabed 
    and wave surfaces.

    Parameters:
        x_grid (np.ndarray): 2D array of X coordinates.
        y_grid (np.ndarray): 2D array of Y coordinates.
        bed_elevation (np.ndarray): Initial seabed elevation (zb).
        seabed_clipped (np.ndarray): Seabed clipped at zero (zb_relu).
        wave_height_initial (np.ndarray): Wave height at first timestep (H[0]).
        target_vertical_fraction (float): Fraction of horizontal extent used 
        to exaggerate vertical scale.

    Returns:
        bed_points (np.ndarray): Recentered and exaggerated seabed 3D points.
        wave_points (np.ndarray): Recentered and exaggerated initial wave 
        3D points (Nx3).
        grid_dimensions (Tuple[int, int, int]): Dimensions for structured grid 
        (nx, ny, 1).
        min_z (float): Minimum z-value of bed elevation (used for exaggeration).
        vertical_exaggeration (float): Vertical exaggeration factor.
        center_x (float): Center of X grid.
        center_y (float): Center of Y grid.
    """
    num_rows, num_cols = x_grid.shape
    flat_x = x_grid.ravel(order='C')
    flat_y = y_grid.ravel(order='C')
    flat_bed = bed_elevation.ravel(order='C')
    flat_wave = (seabed_clipped + wave_height_initial).ravel(order='C')

    center_x = flat_x.mean()
    center_y = flat_y.mean()

    min_z = flat_bed.min()
    max_z = flat_bed.max()
    horizontal_extent = max(np.ptp(flat_x), np.ptp(flat_y))
    vertical_extent = max_z - min_z or 1e-6  # avoid divide by zero

    vertical_exaggeration = (horizontal_extent /
                             vertical_extent) * target_vertical_fraction

    # Center X/Y and apply exaggeration to Z
    bed_points = np.column_stack(
        (flat_x - center_x, flat_y - center_y,
         (flat_bed - min_z) * vertical_exaggeration + min_z))

    wave_points = np.column_stack(
        (flat_x - center_x, flat_y - center_y,
         (flat_wave - min_z) * vertical_exaggeration + min_z))

    grid_dimensions = (num_cols, num_rows, 1)

    return PointCloudData(bed_points=bed_points,
                          wave_points=wave_points,
                          grid_dimensions=grid_dimensions,
                          min_z=min_z,
                          vertical_exaggeration=vertical_exaggeration,
                          center_x=center_x,
                          center_y=center_y)


def update_wave_points(base_xy: np.ndarray, Zs: np.ndarray, H_t: np.ndarray,
                       min_z: float, exag: float) -> np.ndarray:
    """
    Given flattened X/Y (base_xy shape=(N,2)), seabed clip Zs, 
    and a single wave-height slice H_t, compute new 3D points.
    """
    # base_xy[:,0], base_xy[:,1], then new z
    flat_wave = (Zs + H_t).ravel(order='C')
    z_vals = (flat_wave - min_z) * exag + min_z
    return np.column_stack((base_xy[:, 0], base_xy[:, 1], z_vals))


def iterate_time_steps(pc: PointCloudData, Zs: np.ndarray,
                       H: np.ndarray) -> Iterator[np.ndarray]:
    """
    Yields one wave‐point‐cloud per time step.
    """
    # pre‐flattened XY
    base_xy = pc.wave_points[:, :2]
    for t in range(H.shape[0]):
        yield update_wave_points(base_xy, Zs, H[t], pc.min_z,
                                 pc.vertical_exaggeration)


def animate_wave(ds, out_file="wave.mp4", angle=(30, -135), fps=10):
    sim = get_simulation_variables(ds)

    X, Y, Zb, Zs, H = sim["X"], sim["Y"], sim["Zb"], sim["Zs"], sim["H"]

    point_cloud_data = prepare_point_clouds(X, Y, Zb, Zs, H[0])
    dims = point_cloud_data.grid_dimensions
    z_min = point_cloud_data.min_z
    exag = point_cloud_data.vertical_exaggeration

    seabed = _build_structured_grid(point_cloud_data.bed_points, dims,
                                    "elevation")
    wave = _build_structured_grid(point_cloud_data.wave_points, dims, "wave")

    plotter = pv.Plotter(off_screen=True, window_size=(1200, 800))
    plotter.open_movie(out_file, framerate=fps, codec="libx264", quality=10)
    plotter.add_mesh(seabed,
                     scalars="elevation",
                     cmap=sim["seabed_cmap"],
                     show_scalar_bar=False)
    actor = plotter.add_mesh(wave,
                             scalars="wave",
                             cmap=sim["ocean_cmap"],
                             opacity=0.7,
                             show_scalar_bar=False)
    time_text = plotter.add_text("",
                                 position="upper_left",
                                 font_size=12,
                                 color="black")

    elev, azim = angle
    cam_vec = (
        math.cos(math.radians(azim)) * math.cos(math.radians(elev)),
        math.sin(math.radians(azim)) * math.cos(math.radians(elev)),
        math.sin(math.radians(elev)),
    )
    plotter.view_vector(cam_vec)
    plotter.camera.zoom(1.2)
    plotter.render()
    plotter.write_frame()

    for t, pts in enumerate(iterate_time_steps(point_cloud_data, Zs, H)):
        wave.points = pts

        plotter.remove_actor(actor)
        actor = plotter.add_mesh(wave,
                                 scalars="wave",
                                 cmap=sim["ocean_cmap"],
                                 opacity=0.7,
                                 show_scalar_bar=False)
        time_text.set_text(
            text=f"t = {sim['times'][t]:.1f} s | Step = {t}",
            position="upper_left",
        )
        plotter.render()
        plotter.write_frame()

    plotter.close()
    print(f"Saved animation to {out_file}")


def export_vtk_sequence(ds,
                        vtk_dir: str = "VTK",
                        target_vertical_fraction: float = 0.2,
                        wave_prefix: str = "wave") -> None:
    """
    Export a single seabed mesh plus a time-series of wave meshes to VTK files.

    Parameters:
        ds (xr.Dataset): your XBeach netcdf dataset.
        vtk_dir (str): directory to write .vtk files into.
        target_vertical_fraction (float): same exaggeration fraction
        used in prepare_point_clouds.
        wave_prefix (str): prefix for wave filenames (e.g. 'wave_0000.vtk').
    """
    # 1) pull simulation arrays
    sim = get_simulation_variables(ds)
    X, Y, Zb, Zs, H = sim["X"], sim["Y"], sim["Zb"], sim["Zs"], sim["H"]

    # 2) prepare the point clouds (initial wave step)
    pc = prepare_point_clouds(X, Y, Zb, Zs, H[0], target_vertical_fraction)

    # 3) make output directory
    out_path = pathlib.Path(vtk_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 4) write static seabed
    seabed_grid = _build_structured_grid(pc.bed_points, pc.grid_dimensions,
                                         "elevation")
    seabed_file = out_path / "seabed.vtk"
    seabed_grid.save(str(seabed_file))
    print(f"  • Wrote seabed mesh → {seabed_file}")

    nt = H.shape[0]
    for t, pts in enumerate(iterate_time_steps(pc, Zs, H)):
        wave_grid = _build_structured_grid(pts, pc.grid_dimensions,
                                           "wave_height")

        fname = out_path / f"{wave_prefix}_{t:04d}.vtk"
        wave_grid.save(str(fname))
        if t % 10 == 0 or t == nt - 1:
            print(f"  • Wrote frame {t+1}/{nt} → {fname}")

    print(f"All VTK meshes saved in: {out_path.resolve()}")

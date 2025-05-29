import numpy as np
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm


def open_netcdf_file(netcdf_file: str) -> xr.Dataset:
    try:
        return xr.open_dataset(netcdf_file)
    except Exception as e:
        raise ValueError(f"Error opening netcdf file {netcdf_file}: {e}")


def _get_terrain_and_ocean_colormaps(Zmin, Zmax):
    seabed_cmap = LinearSegmentedColormap(
        "black_to_dirt", {
            "red": [(0.0, 0.0, 0.0), (0.5, 0.3, 0.3), (1.0, 0.96, 0.96)],
            "green": [(0.0, 0.0, 0.0), (0.5, 0.2, 0.2), (1.0, 0.87, 0.87)],
            "blue": [(0.0, 0.0, 0.0), (0.5, 0.2, 0.2), (1.0, 0.70, 0.70)],
        })

    ocean_cmap = LinearSegmentedColormap(
        "ocean", {
            "red": [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)],
            "green": [(0.0, 0.0, 0.5), (1.0, 0.5, 1.0)],
            "blue": [(0.0, 0.3, 1.0), (1.0, 1.0, 1.0)],
        })

    norm = TwoSlopeNorm(vmin=Zmin, vcenter=0.0, vmax=Zmax)

    return {
        "seabed_cmap": seabed_cmap,
        "ocean_cmap": ocean_cmap,
        "seabed_norm": norm,
        "ocean_norm": norm
    }


def get_simulation_variables(ds: xr.Dataset, stride: int = 1) -> dict:
    X = ds["globalx"].values[::stride, ::stride]
    Y = ds["globaly"].values[::stride, ::stride]

    Zb = ds["zb"].isel(globaltime=0).values[::stride, ::stride]
    Zs = Zb.clip(min=0)

    H = ds["H"].values[:, ::stride, ::stride]

    times = ds["globaltime"].values

    Zmin, Zmax = Zb.min(), (Zb + np.nanmax(H)).max()

    return {
        "X": X,
        "Y": Y,
        "Zb": Zb,
        "Zs": Zs,
        "H": H,
        "times": times,
        "Zmin": Zmin,
        "Zmax": Zmax,
        **_get_terrain_and_ocean_colormaps(Zmin, Zmax)
    }

# XBeach Visualization and VTK Export CLI

This repository provides a Python command-line tool to visualize XBeach simulations and export VTK meshes:

* **Animate wave** with PyVista
* **Export** seabed and wave time-series as VTK files

## Features

* Supports local results directory (`inputs/` + `outputs/` subfolders)
* Fetches simulation data by **task ID** using `inductiva` API
* Caches downloads and avoids re-downloading unless `--overwrite-downloads` is specified


## Requirements

* Python 3.11+
* `numpy`, `xarray`, `matplotlib`, `pyvista`
* `inductiva` Python package (for task download)
* `xbTools` with `XBeachModelAnalysis` class

Install dependencies via:

```bash
pip install -r requirements.txt
```

## CLI Usage

```bash
python xbeach_animator.py ( SOURCE ) [options]
```

### Required arguments (one of)

* `--results-dir /path/to/results`

  Path to a folder containing:

  ```
  results/
  ├─ inputs/
  │   └─ <sim_dir>/
  └─ outputs/
  ```

* `--input-dir /path/to/inputs --output-dir /path/to/outputs`

  Two separate flat directories—one with all inputs, one with all outputs.

* `--task-id <task_id>`

  Fetches and caches data via `inductiva.tasks.Task`.

### Options

* `--animate-wave`
  Generate a PyVista animation (`wave.mp4` by default).

* `--export-vtk`
  Export a static `seabed.vtk` and `wave_####.vtk` sequence into `--vtk-dir`.

* `--fps <int>` (default: 10)
  Frames per second for the animation.

* `--angle ELEV AZIM` (default: `30 -45`)
  Camera elevation and azimuth angles in degrees.

* `--vtk-dir /path/to/VTK` (default: `VTK`)
  Output folder for VTK meshes.

* `--vertical-fraction <float>` (default: 0.2)
  Vertical exaggeration fraction for both animation and VTK export.

* `--overwrite-downloads`
  Force re-downloading inputs/outputs when using `--task-id`.

## Examples

```bash
# 1) Separate input/output dirs:
python xbeach_animator.py \
  --input-dir /data/run123/inputs \
  --output-dir /data/run123/outputs \
  --animate-wave

# 2) Single results folder:
python xbeach_animator.py \
  --results-dir /data/run123 \
  --export-vtk

# 3) By task ID, both actions with custom fps & camera angle:
python xbeach_animator.py \
  --task-id fwwurpniv7tqi7z37a1iiay2u \
  --animate-wave --export-vtk \
  --fps 5 --angle 45 -30
```

## Repository Structure

```
project-root/
├── xbeach_animator.py   # CLI entrypoint
├── data_processing.py   # NetCDF loading & variable extraction
├── visualization.py     # PyVista animation & VTK export
├── README.md            # This documentation
└── requirements.txt     # Pin dependencies
```

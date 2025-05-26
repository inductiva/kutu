import vtk
import numpy as np
from numba import njit
from vtk.util.numpy_support import vtk_to_numpy
from skimage import measure
import os
import argparse
from concurrent.futures import ThreadPoolExecutor

def vtk_to_points(vtk_file):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtk_file)
    reader.Update()
    data = reader.GetOutput()
    points = vtk_to_numpy(data.GetPoints().GetData())
    return points

@njit
def create_density_field(points, grid_size=500, radius=0.005):
    field = np.zeros((grid_size, grid_size, grid_size), dtype=np.float32)
    spacing = 1.0 / grid_size
    r2 = radius * radius
    sigma2 = (radius / 2) ** 2
    n_points = points.shape[0]

    for p_idx in range(n_points):
        px, py, pz = points[p_idx]
        i, j, k = int(px / spacing), int(py / spacing), int(pz / spacing)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                for dz in range(-2, 3):
                    ni, nj, nk = i + dx, j + dy, k + dz
                    if 0 <= ni < grid_size and 0 <= nj < grid_size and 0 <= nk < grid_size:
                        gx = ni * spacing
                        gy = nj * spacing
                        gz = nk * spacing
                        dist2 = (gx - px)**2 + (gy - py)**2 + (gz - pz)**2
                        if dist2 < r2:
                            field[ni, nj, nk] += np.exp(-dist2 / (2 * sigma2))
    return field

def mesh_from_field(field, iso=0.5):
    verts, faces, _, _ = measure.marching_cubes(field, level=iso)
    return verts, faces

def save_obj(filename, verts, faces):
    with open(filename, 'w') as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {int(face[0]+1)} {int(face[1]+1)} {int(face[2]+1)}\n")

def process_file(vtk_file, out_dir, iso, grid_size, radius):
    try:
        print(f"[START] Processing {vtk_file}")
        points = vtk_to_points(vtk_file)
        field = create_density_field(points, grid_size=grid_size, radius=radius)
        verts, faces = mesh_from_field(field, iso=iso)
        frame_id = os.path.splitext(os.path.basename(vtk_file))[0]
        save_obj(os.path.join(out_dir, f"{frame_id}.obj"), verts, faces)
        print(f"[DONE] {vtk_file} → mesh")
    except Exception as e:
        print(f"[ERROR] Failed to process {vtk_file}: {e}")

def convert_vtk_dir_to_meshes(vtk_dir, out_dir, iso=0.5, grid_size=500, radius=0.005, max_workers=None, prefix="PartStructure"):
    os.makedirs(out_dir, exist_ok=True)
    vtk_files = [
        os.path.join(vtk_dir, file)
        for file in sorted(os.listdir(vtk_dir))
        if file.endswith('.vtk') and file.startswith(prefix)
    ]

    if max_workers is None:
        max_workers = os.cpu_count() or 4

    def task(vtk_file):
        process_file(vtk_file, out_dir, iso, grid_size, radius)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task, file) for file in vtk_files]
        for future in futures:
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .vtk files to mesh .obj files.")
    parser.add_argument("vtk_dir", help="Path to input directory containing .vtk files")
    parser.add_argument("out_dir", help="Path to output directory for .obj meshes")
    parser.add_argument("--iso", type=float, default=0.5, help="Isosurface threshold for marching cubes")
    parser.add_argument("--prefix", type=str, default="PartStructure", help="Filename prefix filter for .vtk files (default: PartStructure)")
    parser.add_argument("--grid-size", type=int, default=500, help="Grid resolution for the density field")
    parser.add_argument("--radius", type=float, default=0.005, help="Influence radius for point density")
    parser.add_argument("--max-workers", type=int, default=None, help="Maximum number of parallel threads (default: CPU count)")

    args = parser.parse_args()

    convert_vtk_dir_to_meshes(
        args.vtk_dir,
        args.out_dir,
        iso=args.iso,
        grid_size=args.grid_size,
        radius=args.radius,
        max_workers=args.max_workers,
        prefix=args.prefix
    )
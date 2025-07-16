import os
import re
import vtkmodules.all as vtk
from vtkmodules.util import numpy_support
import numpy as np
import imageio
import argparse


def read_vtk(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()


def create_actor(dataset, color):
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(dataset)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetDiffuse(0.8)
    actor.GetProperty().SetSpecular(0.3)
    actor.GetProperty().SetSpecularPower(20)
    return actor


def create_glyph_actor(dataset, radius, color):
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetRadius(radius)
    sphere_source.SetThetaResolution(5)
    sphere_source.SetPhiResolution(5)
    sphere_source.Update()

    glyph = vtk.vtkGlyph3D()
    glyph.SetSourceConnection(sphere_source.GetOutputPort())
    glyph.SetInputData(dataset)
    glyph.SetScaleModeToDataScalingOff()
    glyph.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetDiffuse(0.8)
    actor.GetProperty().SetSpecular(0.3)
    actor.GetProperty().SetSpecularPower(20)
    actor.GetProperty().SetInterpolationToPhong()
    return actor


def numeric_key(filename):
    match = re.search(r'_(\d+)\.vtk$', filename)
    if match:
        return int(match.group(1))
    else:
        return -1


def render_to_image(render_window):
    window_to_image = vtk.vtkWindowToImageFilter()
    window_to_image.SetInput(render_window)
    window_to_image.Update()

    vtk_image = window_to_image.GetOutput()
    width, height, _ = vtk_image.GetDimensions()

    vtk_array = vtk_image.GetPointData().GetScalars()
    components = vtk_array.GetNumberOfComponents()
    arr = numpy_support.vtk_to_numpy(vtk_array).reshape(height, width, components)
    arr = np.flip(arr, 0)
    return arr


def main(folder_path, output_gif, cam_pos, cam_fp):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.vtk')],
                   key=numeric_key)

    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.SetOffScreenRendering(1)
    render_window.AddRenderer(renderer)
    render_window.SetSize(600, 600)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    images = []

    for f in files:
        renderer.RemoveAllViewProps()

        polydata = read_vtk(os.path.join(folder_path, f))
        color = (0.1, 0.4, 0.8)
        actor = create_glyph_actor(polydata, radius=0.015, color=color)
        renderer.AddActor(actor)

        renderer.SetBackground(1, 1, 1)

        renderer.ResetCamera()
        camera = renderer.GetActiveCamera()
        camera.SetPosition(*cam_pos)
        camera.SetFocalPoint(*cam_fp)
        camera.SetViewUp(0, 1, 0)
        renderer.ResetCameraClippingRange()
        render_window.Render()

        img = render_to_image(render_window)
        images.append(img)

    imageio.mimsave(output_gif, images, loop=0, duration=0.2)
    print(f"GIF saved to {output_gif}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render VTK frames into a GIF with custom camera view.")
    parser.add_argument("folder", help="Folder containing .vtk files.")
    parser.add_argument("output", help="Output GIF path.")
    parser.add_argument("--cam_pos", type=float, nargs=3, default=[4.0, 1.0, 4.0],
                        help="Camera position: x y z (default: 4 1 4)")
    parser.add_argument("--cam_fp", type=float, nargs=3, default=[0.0, 0.0, 0.0],
                        help="Camera focal point: x y z (default: 0 0 0)")

    args = parser.parse_args()

    main(args.folder, args.output, args.cam_pos, args.cam_fp)

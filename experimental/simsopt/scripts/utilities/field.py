"""Utilities for the magnetic field calculation."""
from simsopt import field, mhd


def get_plasma_surface_from_vmec_file(plasma_surface_file_path,
                                      num_phi,
                                      num_theta,
                                      verbose=False):
    """Gets the boundary surface from a Vmec file.

    Creates the `Vmec` object and obtains its boundary surface defined with 
    a resolution of num_phi in the toroidal direction (long way around the 
    torus) and a resolution of num_theta in the poloidal direction (short way
    around the torus).

    Args:
        plasma_surface_file_path (str): Vmec input file with the plasma 
          description
        verbose (bool): Prints the output of the Vmec object creation
          when true.
        num_phi (int): Toroidal resolution for the Biot-Savart magnetic field.
        num_theta (int): Toroidal resolution for the Biot-Savart magnetic field.

    Returns:
        plasma_surface (Vmec boundary): Surface for the magnetic field
          calculation.
    """

    vmec = mhd.Vmec(plasma_surface_file_path,
                    verbose=verbose,
                    nphi=num_phi,
                    ntheta=num_theta)
    plasma_surface = vmec.boundary

    return plasma_surface


def get_magnetic_field_vector(plasma_surface, coils_lst):
    """Calculates the magnetic field vector produced by the coils.

    Calculates the magnetic field in a set of points on a given 
    surface (plasma surface).

    Args:
        plasma_surface (Vmec boundary): Description of the plasma surface
          with a certain resolution for the calculation of the magnetic field.
        coils_lst (simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        magnetic_field: Numpy matrix with the magnetic field vector
          in each point. The number of columns is 3 for each component of the
          vector. 
    """

    # Setup
    biot_savart = biot_savart_setup(plasma_surface, coils_lst)

    # Calculates the magnetic field.
    magnetic_field = biot_savart.B()

    return magnetic_field


def get_magnetic_field_abs(plasma_surface, coils_lst):
    """Calculates the magnetic field strength produced by the coils.

    Calculates the magnetic field in a set of points on a given 
    surface (plasma surface).

    Args:
        plasma_surface (Vmec boundary): Description of the plasma surface
          with a certain resolution for the calculation of the magnetic field.
        coils_lst (simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        magnetic_field: Magnetic field strength in each point.
    """

    # Setup
    biot_savart = biot_savart_setup(plasma_surface, coils_lst)

    # Calculates the magnetic field strength
    magnetic_field = biot_savart.AbsB()

    return magnetic_field


def biot_savart_setup(plasma_surface, coils_lst):
    """Setup for the magnetic field calculation.

    Creates the simsopt `BiotSavart` object for the
    later calculation of the magnetic field.

    Args:
        plasma_surface (Vmec boundary): Boundary surface of a plasma description
          with a certain resolution for the calculation of the magnetic field.
        coils_lst (simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        biot_savart (BiotSavart): Simsopt BiotSavart object.
    """

    # Creates the Biot-Savart object.
    biot_savart = field.BiotSavart(coils_lst)

    # Sets the points for the field calculation.
    # Surface.gamma() returns the coordinates of the surface. They are then
    # converted to a matrix with 3 columns (one for each coordinate).
    biot_savart.set_points(plasma_surface.gamma().reshape((-1, 3)))

    return biot_savart

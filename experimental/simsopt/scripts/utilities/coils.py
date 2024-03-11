"""Utilities for the coil creation."""
from simsopt import field, geo


def create_curve_from_coefficients(curve_coefficients, points_multiplier):
    """Creates simsopt curve object from coefficients arrays.

    Args: 
        curve_coefficients (np.ndarray): Array with Fourier coefficients 
          defining the curve. Shape (6, max_order + 1), where `max_order`
          is the maximum order of Fourier coefficients in the
          `curve_coefficients` array.
        points_multiplier (int): Multiplier for the number of 
          points defining the coils for magnetic field calculation.  
          The total number of points that defines a curve is 
          `points_multiplier*max_order`.

    Returns:
        curve (simsopt.geo.curvexyzfourier.CurveXYZFourier curve): The resulting 
          simsopt curve object.
    """

    # Gets the maximum order of the Fourier Series coefficients.
    max_order = curve_coefficients.shape[1] - 1

    # Number of points to define the curve.
    points = points_multiplier * max_order

    curve = geo.curvexyzfourier.CurveXYZFourier(points, max_order)

    for order in range(max_order + 1):
        curve.set(f'xc({order})', curve_coefficients[1, order])
        curve.set(f'yc({order})', curve_coefficients[3, order])
        curve.set(f'zc({order})', curve_coefficients[5, order])

        # sin(0)=0, so there are no sin coefficients for order zero.
        if order != 0:
            curve.set(f'xs({order})', curve_coefficients[0, order])
            curve.set(f'ys({order})', curve_coefficients[2, order])
            curve.set(f'zs({order})', curve_coefficients[4, order])

    curve.x = curve.x  # Needed to transfer data to C++ in simsopt.

    return curve


def create_coils(curves_coefficients, coil_currents, points_multiplier,
                 num_field_periods):
    """Creates the full set of coils.

    Given the curve coefficients and currents creates the coils after applying
    num_field_periods (nfp) rotational symmetry and stellarator  
    symmetry. Final number of coils = num_coils*nfp*2

    Args:
        curve_coefficients (list): List of numpy arrays with Fourier 
          coefficients defining the curves.
        coil_currents (np.ndarray): Array with the current in each coil.
        points_multiplier (int): Multiplier for the number of 
          points defining the coils for magnetic field calculation.  
          The total number of points that defines a curve is 
          `points_multiplier*max_order`, where max_order is the maximum 
          order of Fourier coefficients in the `curve_coefficients` array.
        num_field_periods (int): Number of magnetic field periods.
          Refers to the number of complete magnetic field repetitions 
          within a stellarator. Represents how many times the magnetic
          field pattern repeats itself along the toroidal direction.

    Returns:
        coils (simsopt coils): Final set of coils.
    """

    curves = [
        create_curve_from_coefficients(coefficients, points_multiplier)
        for coefficients in curves_coefficients
    ]

    currents = [field.Current(current) for current in coil_currents]

    stellarator_symmetry = True
    coils = field.coils_via_symmetries(curves, currents, num_field_periods,
                                       stellarator_symmetry)

    return coils

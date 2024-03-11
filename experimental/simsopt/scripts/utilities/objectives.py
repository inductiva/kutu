"""Stellarator objective functions.

This functions are calculated using the Simsopt software methods. Simsopt
is a framework mainly used for optimizing stellarators. Therefore, usually,
these functions are primarily used to assist in the common optimization 
process that guides the design of these stellarator devices. 
For more information about the Simsopt software be sure to check out the 
`SimsoptExecuter` docstring in the `simulation.py` script and also the 
software's github page at: https://github.com/hiddenSymmetries/simsopt

Despite normally being used to assist the optimization of stellarator
devices, these functions can also be used to assess parameters related
with the quality of performance and with the complexity of construction 
of the device, which are key when creating actual physical devices. 
On one hand, the performance of the device ought to be as good as 
possible, to ensure optimal plasma confinement and energy production, 
satisfying the desired physical qualities of a stellarator. This 
is measured through, for example, the 'Squared Flux' function. 
On the other hand, designing these devices is also an engineering challenge.
Therefore, simplicity can be as valuable as optimal performance, due to the 
fact that many configurations are unfeasible (or even just plain impossible) 
to reproduce, because of the very high coil complexity, rendering their 
potential high performance useless. This can be measured through, for example, 
the 'Coils length' and the 'Mean Squared Curvature' functions.

Simsopt's objective functions have two methods, the `J` method and the `dJ`
method. The second one is not important when assessing the quality of the 
device, given that it only calculates the derivative of a certain quantity
with respect to the degrees of freedom that define the stellarator coils, 
being extremely important in optimization scenarios. The `J` method returns
the value of the objective function, a scalar, that can be used to compare
between different devices, being extremely important in the assessment process.
In this file, some functions are designed to retrieve this exact value from 
the Simsopt objective functions, so they can be used to assess the quality
of the devices. These functions are identifiable with the prefix `get`.
There are also functions to create the objectives, so that they can be used
in the previously mentioned functions. These are identifiable with the prefix
`create`.
"""
import numpy as np
import simsopt

from . import field


def get_squared_flux(plasma_surface, coils_lst, definition='local'):
    r"""Calculates the Squared Flux objective function.

    This cost function measures the deviation between the magnetic field 
    produced by the coils and the wanted magnetic field on the plasma surface, 
    which should be, in all points, completely tangent. 

    This deviation is measured by calculating, on each point that defines the 
    surface, the square of the dot product between the magnetic field produced 
    by the coils, B, and the normal vector of the plasma surface, n. The 
    contribution from all the points is added to produce the final result. This 
    result could have a normalization depending on the `definition` parameter.

    `definition='quadratic flux'`:

    $\int_{S} (\mathbf{B} \cdot \mathbf{n})^2 dS$

    `definition='normalized'`:

    $\frac{\int_{S} (\mathbf{B} \cdot \mathbf{n})^2 dS} 
          {\int_{S} |\mathbf{B}|^2 dS}$

    `definition='local'`:

    $\int_{S} \frac{(\mathbf{B} \cdot \mathbf{n})^2}{|\mathbf{B}|^2} dS$

    Args:
        plasma_surface (Vmec boundary): Boundary surface of a plasma description
          with a certain resolution for the calculation of the magnetic field.
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        definition (str): What kind of operation to perform. The available 
          options are 'quadratic flux', 'local' and 'normalized'.

    Returns:
        Value of the objective function (non-negative scalar).
    """

    # Check if the provided `definition` is valid
    if definition not in ['quadratic flux', 'normalized', 'local']:
        raise ValueError(
            'Invalid "definition" argument. '
            'Must be one of: "quadratic flux", "normalized", "local"')

    biot_savart = field.biot_savart_setup(plasma_surface=plasma_surface,
                                          coils_lst=coils_lst)

    return simsopt.objectives.SquaredFlux(plasma_surface,
                                          biot_savart,
                                          definition=definition).J()


def get_coils_length(coils_lst):
    r"""Calculates the total length of a set of coils.

    Computes the total length of the full set of coils of the stellarator 
    device. 

    The calculation is performed using:

    $\int_{\text{curve}} dl$

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        Total length of the set of coils (scalar).
    """

    # Get the curve length for each curve.
    curves_length = [
        create_simsopt_curve_length_objective(coil) for coil in coils_lst
    ]

    # Get the total length of the set of coils.
    total_length = sum(curves_length)

    return float(total_length.J())


def get_coils_length_penalty(coils_lst, length_threshold):
    r"""Calculates a penalty for the length of the coils.

    Computes a penalty function for each coil given a threshold limit for 
    the length.

    The calculation is performed using:

    $\0.5(\text{obj}.J() - \text{length_threshold})^2$
    
    There `obj` refers to the simsopt.geo.CurveLength object, meaning that 
    `obj.J()` simply denotes the length of the particular coil.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        length_threshold (float): Threshold limit for the length of each coil.

    Returns:
        Total penalty for the set of coils (scalar).
    """

    # Get the curve length for each curve.
    curves_length = [
        create_simsopt_curve_length_objective(coil) for coil in coils_lst
    ]

    # Calculate the quadratic penalty in relation to the given length threshold
    # for each coil.
    quadratic_penalty = [
        simsopt.objectives.QuadraticPenalty(length, length_threshold)
        for length in curves_length
    ]

    return sum(quadratic_penalty).J()


def create_simsopt_curve_length_objective(coil):
    r"""Creates the simsopt objective with the length of a coil.

    Creates a simsopt.geo.CurveLength object with the information of the
    length of the coil of the stellarator device. The object's 
    `J` method returns the length of the coil. 
    Therefore, it is essential to create this object in order to access 
    the length quantity (via `J`) in the `coils_length` function.  
    The object is also used in the `coils_length_penalty_objective` function.

    The calculation of the length is performed using:

    $\int_{\text{curve}} dl$

    Args:
        coil (simsopt Coil object): Eletromagnetic coil.

    Returns:
        length (simsopt.geo.CurveLength object): The objective function being
          returned. To access its length value use `J`.
    """

    # Get the curve that defines the coil because the simsopt
    # `CurveLength` function takes simsopt curve as an argument.
    curve = coil.curve

    # Get the curve length object
    length = simsopt.geo.CurveLength(curve)

    return length


def get_mean_squared_curvature(coils_lst):
    r"""Calculates the total mean squared curvature of a set of coils.

    The calculation is performed, for each coil, using:

    $(1/L) \int_{\text{curve}} \kappa^2 dl$

    where $L$ is the length of the coil, $dl$ is the incremental arclength
    and $\kappa$ is the coil's curvature.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        Total mean squared curvature of the set of coils (scalar).
    """

    # Get the mean squared curvature objective for each curve.
    mean_squared_curvatures = [
        create_simsopt_mean_squared_curvature_objective(coil)
        for coil in coils_lst
    ]

    # Get the total mean squared curvature of the set of coils.
    total_mean_squared_curvature = sum(mean_squared_curvatures)

    return total_mean_squared_curvature.J()


def get_mean_squared_curvature_penalty(coils_lst,
                                       mean_squared_curvature_threshold):
    r"""Calculates a penalty for the mean squared curvature of the coils.

    Computes a penalty function for each coil given a threshold limit for 
    the mean squared curvature and returns the total penalty for the full set.

    The calculation is performed using:

    $\0.5(\text{obj}.J() - \text{length_threshold})^2$
    
    There `obj` refers to the simsopt.geo.MeanSquaredCurvature object, meaning 
    that `obj.J()` simply denotes the mean squared curvature of the particular 
    coil.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        mean_squared_curvature_threshold (float): Threshold limit for the mean 
          squared curvature of each coil.

    Returns:
        Total penalty for the set of coils (scalar).
    """

    # Get the Mean Squared Curvature objective for each coil.
    mean_squared_curvatures = [
        create_simsopt_mean_squared_curvature_objective(coil)
        for coil in coils_lst
    ]

    # Calculate the quadratic penalty in relation to the given threshold
    # for each coil.
    quadratic_penalty = [
        simsopt.objectives.QuadraticPenalty(msc,
                                            mean_squared_curvature_threshold)
        for msc in mean_squared_curvatures
    ]

    return sum(quadratic_penalty).J()


def create_simsopt_mean_squared_curvature_objective(coil):
    r"""Creates the simsopt objective with the mean squared curvature of a coil.

    Create a simsopt.geo.MeanSquaredCurvature object with the information of the
    mean squared curvature of the coil of the stellarator device. The object's 
    `J` method returns the mean squared curvature of the coil. 
    Therefore, it is essential to create this object in order to access 
    the quantity (via `J`) in the `get_mean_squared_curvature` function.  
    The object is also used in the `get_mean_squared_curvature_penalty` 
    function.

    The calculation of the mean squared curvature is performed using:

    $(1/L) \int_{\text{curve}} \kappa^2 dl$

    where $L$ is the length of the coil, $dl$ is the incremental arclength
    and $\kappa$ is the coil's curvature.

    Args:
        coil (simsopt Coil object): Eletromagnetic coil.

    Returns:
        length (simsopt.geo.MeanSquaredCurvature object): The objective 
          function being returned. To access its value use `J`.
    """

    # Get the curve that defines the coil because the simsopt
    # `MeanSquaredCurvature` function takes simsopt curve as an argument.
    curve = coil.curve

    # Get the mean squared curvature objective.
    mean_squared_curvature = simsopt.geo.MeanSquaredCurvature(curve)

    return mean_squared_curvature


def get_arclength_variation(coils_lst):
    r"""Calculates the total arclength variation of a set of coils.

    Each coil is computationally discretized by smaller segments, where the 
    number of segments is determined by the number of quadrature points 
    defining the coil. This function calculates the arclength of each one of 
    this segments and then calculates the variance between those values.

    Ideally, the value obtained would be zero, meaning that all the segments of
    the coil's curve would have exactly the same arclength. This calculation 
    is important in stellarator designs given that the design of the coils 
    is an ill-posed problem, if one wants them to produce a specific magnetic
    field. This is due to the fact that there exists several different sets of
    coils that produced the same magnetic field. Therefore, there is a certain
    non-uniqueness of the coil parametrization.

    The calculation is performed, for each coil, using:

    $\mathrm{Var}(dl_i)$

    where $dl_i$ is the arclength of each segment $i$ of the coil.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        Total arclength variation of the set of coils (scalar).
    """

    # Get the arclength variation for each curve.
    arclength_variation = [
        simsopt.geo.ArclengthVariation(coil.curve) for coil in coils_lst
    ]

    # Get the total arclength variation of the set of coils.
    total_arclength_variation = sum(arclength_variation)

    return total_arclength_variation.J()


def get_coils_curvature_penalty(coils_lst, curvature_threshold, p_norm_value=2):
    r"""Calculates a penalty for the curvature of the coils.

    Computes a penalty function for each coil given a threshold limit for 
    the curvature.

    The calculation is performed using:

    $\frac{1}{p} \int_{\text{curve}} 
    \text{max}(\kappa - curvature_threshold, 0)^p dl$,

    where $p$ is given by `p_norm_value` (check the arguments description for 
    more information) and $\kappa$ is the coil's curvature on a given point,
    which is obtained using:

    $\kappa=
    \frac{\left|\mathbf{r}^{\prime} \times \mathbf{r}^{\prime \prime}\right|}
    {\left|\mathbf{r}^{\prime}\right|^3}$

    where $\mathbf{r}$ is the x,y,z coordinates of the point, 
    $\mathbf{r}^{\prime}$ refers to the derivative of $\mathbf{r}$ with 
    respect to $\varphi$, the toroidal angle (long way around the torus),
    and $\mathbf{r}^{\prime \prime}$ refers to the second derivative.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        curvature_threshold (float): Threshold limit for the curvature of 
          each coil.
        p_norm_value (int): Type of norm to use in the calculation of the 
          length/magnitude of a vector. For example, the '2-norm' 
          (`p_norm_value=2`) is merely the common Euclidian space method,
          where $\| \mathbf{r} \|_2 = (x^2 + y^2 + z^2)^{1/2}$. More generally,
          for a certain 'p_norm': 
            $\| \mathbf{r} \|_p = (|x|^p + |y|^p + |z|^p)^{1/p}$.

    Returns:
        Total penalty for the set of coils (scalar).
    """

    # Get the curvature penalty for each curve.
    curvature_penalty = [
        simsopt.geo.LpCurveCurvature(coil.curve, p_norm_value,
                                     curvature_threshold) for coil in coils_lst
    ]

    # Get the total curvature penalty for the set of coils.
    return sum(curvature_penalty).J()


def get_coil_to_coil_distance_penalty(coils_lst,
                                      cc_threshold,
                                      num_base_coils=None):
    r"""Calculates a penalty for the distance bewteen coils.

    Computes a penalty function for the distance between each coil given a 
    threshold limit.

    This is important to calculate due to the fact that in real physical
    devices there needs to exist certain components between adjacent coils
    so that the stellarator can successfully operate.

    It is calculated using:

    $\sum_{i = 1}^{\text{num_coils}} \sum_{j = 1}^{i-1} d_{i,j}$,

    where 

    $d_{i,j} = \int_{\text{curve}_i} \int_{\text{curve}_j} \max(0, 
    cc_{\text{threshold}} - \| \mathbf{r}_i - \mathbf{r}_j \|_2)^2 ~dl_j ~dl_i$

    and $\mathbf{r}_i$, $\mathbf{r}_j$ are points on coils $i$ and 
    $j$, respectively. $cc_{\text{threshold}}$ is a desired threshold minimum 
    intercoil distance.  

    This penalty calculation comes out to zero when the distance between points
    on coil $i$ and coil $j$ is higher than $cc_{\text{threshold}}$ for all 
    coils used in the calculation.

    If `num_base_coils` is passed, then the code only computes the distance to
    the first `num_base_coils` many curves, which is useful in stellarator 
    configurations due to the symmetries involved in the coil creation.
    However, if this argument is not provided, the calculation will be 
    performed for all the coils in the device.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        cc_threshold (float): Threshold limit for the distance between coils.
        num_base_coils (int, optional): Number of coils to use for the 
          computation of the coil to coil distance. This is useful in 
          stellarator configurations due to the symmetries involved. However,
          if not provided, defaults to the number of coils in the entire set.

    Returns:
        Total penalty for the set of coils (scalar).
    """

    if num_base_coils is None:
        num_base_coils = len(coils_lst)

    # Obtain the curves from the coil set.
    curves = [coil.curve for coil in coils_lst]

    # Calculate the Coil to Coil distance penalty.
    return float(
        simsopt.geo.CurveCurveDistance(curves,
                                       cc_threshold,
                                       num_basecurves=num_base_coils).J())


def get_coil_to_surface_distance_penalty(plasma_surface, coils_lst,
                                         cs_threshold):
    r"""Calculates a penalty for the distance bewteen coils and plasma surface.

    Computes a penalty function for the distance between each coil and the 
    surface of the plasma given a threshold limit.

    This is important to calculate due to the fact that in real physical
    devices there needs to exist certain components between the coils and
    the plasma so that the stellarator can successfully operate.

    It is calculated using:

    $\sum_{i = 1}^{\text{num_coils}} d_{i}$,

    where 

    $d_{i} = \int_{\text{curve}_i} \int_{surface} \max(0, 
    cs_{\text{threshold}} - \| \mathbf{r}_i - \mathbf{s} \|_2)^2 ~dS ~dl_i$

    and $\mathbf{r}_i$, $\mathbf{s}$ are points on coil $i$ and the 
    surface, respectively. $cs_{\text{threshold}}$ is a desired threshold
    minimum coil-to-surface distance.
    
    This penalty calculation comes out to zero when the points on all coils
    and on the surface lie more than $cs_{\text{threshold}}$ away from one 
    another.

    Args:
        plasma_surface (Vmec boundary): Boundary surface of a plasma description
          with a certain resolution.
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        cs_threshold (float): Threshold limit for the distance between the coils
          and the plasma surface.

    Returns:
        Total penalty for the set of coils (scalar).
    """

    # Obtain the curves from the coil set.
    curves = [coil.curve for coil in coils_lst]

    # Calculate the Coil to Surface distance penalty.
    return float(
        simsopt.geo.CurveSurfaceDistance(curves, plasma_surface,
                                         cs_threshold).J())


def get_coils_curvature(coils_lst):
    r"""Calculates the curvature of the coils.

    For each coil in `coils_lst` this function calculates the maximum curvature,
    defined at each point of the curve as:

    $\kappa=
    \frac{\left|\mathbf{r}^{\prime} \times \mathbf{r}^{\prime \prime}\right|}
    {\left|\mathbf{r}^{\prime}\right|^3}$

    where $\mathbf{r}$ is the x,y,z coordinates of the point, 
    $\mathbf{r}^{\prime}$ refers to the derivative of $\mathbf{r}$ with 
    respect to $\varphi$, the toroidal angle (long way around the torus),
    and $\mathbf{r}^{\prime \prime}$ refers to the second derivative.

    The values of the maximum curvature of each coil are then all added up
    to be returned by this function as a single scalar value.

    Args:
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.

    Returns:
        Total sum of the maximum curvature of each coil (scalar).
    """

    return sum(np.max(coil.curve.kappa()) for coil in coils_lst)


def get_all_objectives(plasma_surface,
                       coils_lst,
                       objectives_weights,
                       num_base_coils=None):
    """Calculates all the objective functions.

    Returns a dictionary with the values of all the objective functions
    and with a total objective function that combines them. 

    Args:
        plasma_surface (Vmec boundary): Boundary surface of a plasma description
          with a certain resolution.
        coils_lst (list of simsopt Coils objects): Set of eletromagnetic coils.
        objectives_weights (dictionary): Contains the weights of the objective
          functions to use for the construction of the total objective.
        num_base_coils (int, optional): Number of coils to use for the 
          computation of the coil to coil distance. This is useful in 
          stellarator configurations due to the symmetries involved. However,
          if not provided, defaults to the number of coils in the entire set.

    Returns:
        objectives_dict (dictionary): Contains the values of all the objective
          functions.
    """

    if num_base_coils is None:
        num_base_coils = len(coils_lst)

    # Creating an empty dictionary to store the objective function values.
    objectives_dict = {}

    objectives_dict['total'] = 0

    # To calculate the total objective function.
    total_objective = 0

    if 'squared_flux' in objectives_weights:
        squared_flux = objectives_weights['squared_flux'] * get_squared_flux(
            plasma_surface=plasma_surface, coils_lst=coils_lst)

        total_objective += squared_flux
        objectives_dict['squared_flux'] = squared_flux

    if 'coils_length' in objectives_weights:
        length = objectives_weights['coils_length'] * get_coils_length(
            coils_lst=coils_lst)

        total_objective += length
        objectives_dict['coils_length'] = length

    if 'mean_squared_curvature' in objectives_weights:
        msc = objectives_weights[
            'mean_squared_curvature'] * get_mean_squared_curvature(
                coils_lst=coils_lst)

        total_objective += msc
        objectives_dict['mean_squared_curvature'] = msc

    if 'arclength_variation' in objectives_weights:
        arclength = objectives_weights[
            'arclength_variation'] * get_arclength_variation(
                coils_lst=coils_lst)

        total_objective += arclength
        objectives_dict['arclength_variation'] = arclength

    if 'curvature' in objectives_weights:
        curvature = objectives_weights['curvature'] * get_coils_curvature(
            coils_lst=coils_lst)

        total_objective += curvature
        objectives_dict['curvature'] = curvature

    if 'cc_distance' in objectives_weights:
        cc_distance = objectives_weights[
            'cc_distance'] * get_coil_to_coil_distance_penalty(
                coils_lst=coils_lst,
                cc_threshold=0.1,
                num_base_coils=num_base_coils)

        total_objective += cc_distance
        objectives_dict['cc_distance'] = cc_distance

    if 'cs_distance' in objectives_weights:
        cs_distance = objectives_weights[
            'cs_distance'] * get_coil_to_surface_distance_penalty(
                plasma_surface=plasma_surface,
                coils_lst=coils_lst,
                cs_threshold=0.3)
        total_objective += cs_distance
        objectives_dict['cs_distance'] = cs_distance

    # Store the total objective.
    objectives_dict['total'] = total_objective

    return objectives_dict

"""Utility functions to assist the scripts."""
import numpy as np


def generate_noisy_configurations(initial_coefficients, num_samples,
                                  sigma_scaling_factor):
    """Generates new configurations by adding Gaussian noise to an 
    initial configuration.

    Given an initial coil configuration with all the coefficients
    describing their Fourier Series representation, this function
    generates `num_samples` different configurations by adding normal 
    distribution noise to each coefficient. 

    The sigma value of the Gaussian noise applied to each coefficient is 
    determined by multiplying `sigma_scaling_factor` with its absolute value.

    Args:
        initial_coefficients (list of np.ndarrays): List of numpy arrays with 
          Fourier coefficients defining each base coil of the device. For each
          element of this list (each coil) the shape is (6, order + 1), where 
          order is the maximum order of the Fourier Series representation.
        num_samples (int): Number of different stellarator configurations to
          generate.
        sigma_scaling_factor (float): Scaling factor for the sigma value 
          used in the random generation of Normal distribution noise.
          This is such that the noise is proportional relative to the 
          coefficient.

    Returns:
        noisy_coil_configurations (list of lists of np.ndarrays): This list 
          contains `num_samples + 1` lists. Each is a new configuration 
          obtained by adding noise to the initial one, which was also added
          to this list. Therefore, each one of these has as many numpy 
          arrays as base coils in the device. Every one of these arrays 
          has a shape of (6, order + 1), just like in the initial configuration.
    """

    # Copy the initial list to avoid changing it.
    starting_coefficients = initial_coefficients.copy()

    # Convert `starting_coefficients` to a 3D numpy array.
    starting_coefficients = np.array(starting_coefficients)

    # Create the normal distribution noise scaling it based
    # on the value of the corresponding coefficient.
    # `random_noise` is thus a numpy array with shape
    # (`num_samples`, `num_coils`, 6, order + 1).
    noise_levels = sigma_scaling_factor * np.abs(starting_coefficients)
    random_noise = np.random.normal(loc=0,
                                    scale=noise_levels,
                                    size=(num_samples,) +
                                    starting_coefficients.shape)

    # Add an extra dimension to `starting_coefficients` to match the shape of
    # `random_noise`.
    starting_coefficients = np.expand_dims(starting_coefficients, axis=0)

    # Add noise to initial coefficients.
    noisy_coefficients = starting_coefficients + random_noise

    num_coils = noisy_coefficients.shape[1]

    # Stores the generated configurations in a list with size `num_samples`
    # where each element is a list that defines a configuration of coils.
    noisy_coil_configurations = [[
        noisy_coefficients[sample, coil] for coil in range(num_coils)
    ] for sample in range(num_samples)]

    # Insert the initial configuration in the beginning.
    noisy_coil_configurations.insert(0, initial_coefficients)

    return noisy_coil_configurations


def choose_best_coils_configuration(coil_coefficients_set, objectives_lst):
    """Chooses the best stellarator out of a set.

    Given a set of different stellarators whose coefficients are contained in
    `coil_coefficients_set` this function chooses the one with the lowest value
    of the objective function.

    Args:
        coil_coefficients_set (list of lists of np.ndarrays): This list should
          contain a certain number of lists, where each represent a coil 
          configuration. In each configuration there should be as many 
          numpy arrays as base coils in the device, with shape (6, order + 1),
          that refer to the description of each coil of the particular device.
        objectives_list (list of floats): This list contains the values of the
          objective function used to determined the best configuration. 

    Returns:
        best_configuration (list of np.ndarrays): List of numpy arrays with 
          Fourier coefficients defining each base coil of the best device. For 
          each element of this list (each coil) the shape is (6, order + 1), 
          where order is the maximum order of the Fourier Series representation.
        best_configuration_index (int): Index of the best configuration out of 
          the `coil_coefficients_set`.
    """

    # Find the device with the minimum objective value.
    best_configuration_index = objectives_lst.index(min(objectives_lst))
    best_configuration = coil_coefficients_set[best_configuration_index]

    return best_configuration, best_configuration_index

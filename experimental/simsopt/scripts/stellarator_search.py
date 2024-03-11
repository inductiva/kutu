"""Script to search for noise generated stellarator configurations."""
import csv
import json
import os
import shutil

from absl import flags
from absl import logging
from absl import app

import numpy as np

import utilities

FLAGS = flags.FLAGS

flags.DEFINE_string('output_path', 'results',
                    'Path for the directory of the outputs.')
flags.DEFINE_string('coil_coefficients_file_path', 'coils.npz',
                    'Path for the coils Fourier coefficients arrays.')
flags.DEFINE_string('plasma_surface_file_path', 'input.example',
                    'Path for the surface description file.')
flags.DEFINE_string('objectives_weights_file_path', 'objectives.json',
                    'Path for weights of the objective functions.')
flags.DEFINE_integer('num_field_periods', 2,
                     'Number of magnetic field periods.')
flags.DEFINE_string('coil_currents_file_path', 'currents.npz',
                    'Path for the current in each coil.')
flags.DEFINE_integer(
    'points_multiplier', 15, 'Multiplier for the number of points defining\
      the coils for magnetic field calculation.')
flags.DEFINE_bool(
    'verbose', False, 'Prints the output for the Vmec object\
    creation when true.')
flags.DEFINE_integer(
    'num_theta', 35, 'Poloidal resolution for the Biot-Savart\
    magnetic field.')
flags.DEFINE_integer(
    'num_phi', 50, 'Toroidal resolution for the Biot-Savart\
    magnetic field.')
flags.DEFINE_integer('num_samples', 2000,
                     'Number of stellarators to generate with noise.')
flags.DEFINE_integer('num_iterations', 3, 'Number of iterations.')
flags.DEFINE_float(
    'sigma_scaling_factor', 0.06,
    'Scaling factor for the sigma value used in the random\
                    generation of Normal distribution noise.')


def write_csv_header(csv_filename, header):
    """Writes the header of a csv file.
    
    Args:
        csv_filename (str): Name of the file to write to.
        header (list): Contents of the header.
    """

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(header)


def write_csv_iteration_objectives(csv_filename,
                                   iteration,
                                   objectives_lst,
                                   samples=None):
    """Writes the objective functions of an iteration to a csv file.
    
    Args:
        csv_filename (str): Name of the file to write to.
        iteration (int): Current iteration.
        objectives_lst (list of dictionaries): This list contains the values
          of the objective functions to write.
        samples (list): List with the index of the samples. If not provided 
          assigns an index based on the position of the objective in 
          `objectives_lst`.
    """

    if samples is None:
        samples = list(range(len(objectives_lst)))

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for sample, objectives in zip(samples, objectives_lst):

            # Write the first 3 elements of the row (including the total
            # objective function).
            row = [f'{iteration + 1}', f'{sample}']

            # Write the remaining objective functions.
            for key in objectives:
                row.append(f'{objectives[key]:.3f}')

            # Write the row for this iteration and sample.
            writer.writerow(row)


def save_best_configuration(sample_index, output_path, folder_name,
                            num_iterations):
    """Saves the best configuration.

    Uses the index of the best configuration, given by `sample_index`, to 
    find the folder that corresponds to it and copy it to a specific location.
    
    Args:
        sample_index (int): Index of the best stellarator configuration.
        output_path (str): Path for the directory of the outputs.
        folder_name (str): Name of the folder to save this configuration.
        num_iterations (int): Number of iterations of the optimization process.
    """

    best_configuration_path = os.path.join(output_path,
                                           f'iteration_{num_iterations}',
                                           f'sample_{sample_index}')
    best_configuration_new_path = os.path.join(output_path, folder_name)
    shutil.copytree(best_configuration_path, best_configuration_new_path)


def main(_):
    """Searches for an optimal stellarator configuration.
    
    Given an initial coil configuration, an optimization is performed 
    to find a configuration with better performance (lower value of the
    objective function).

    The optimization is performed as follows:
        1. The input coil configuration is used as an initial 
          configuration.
        2. Gaussian noise is added to each coil parameter to produce 
          `num_sample` configurations.
        3. From these configurations, the one with the lowest value of the
          objective functions is selected.
        4. This configuration is then used as an initial configuration for
          the next iteration.
        5. The process is repeated `num_iteration` times.

    The process outputs the Fourier Series coefficients and the magnetic field
    produced by each configuration, as well as the values of the objective
    functions.
    """

    # Retrieve data from files with the initial Fourier coefficients
    # and coil currents.
    loaded_coefficients = np.load(FLAGS.coil_coefficients_file_path)
    loaded_currents = np.load(FLAGS.coil_currents_file_path)

    # To store the loaded arrays.
    curves_coefficients = list(loaded_coefficients.values())
    coil_currents = list(loaded_currents.values())[0]

    # Retrieves the plasma surface (necessary for the calculation of some
    # objective functions) from the input file.
    plasma_surface = utilities.field.get_plasma_surface_from_vmec_file(
        plasma_surface_file_path=FLAGS.plasma_surface_file_path,
        num_phi=FLAGS.num_phi,
        num_theta=FLAGS.num_theta,
        verbose=FLAGS.verbose)

    # Load the JSON data from the file into a dictionary
    with open(FLAGS.objectives_weights_file_path, 'r',
              encoding='utf-8') as json_file:
        objectives_weights = json.load(json_file)

    # Create the csv file to save the values of the objective functions.
    objectives_filename = os.path.join(FLAGS.output_path, 'objectives.csv')
    header = ['iteration', 'sample', 'total']

    for key in objectives_weights:
        header.append(key)

    write_csv_header(csv_filename=objectives_filename, header=header)

    for iteration in range(FLAGS.num_iterations):

        # Create the directory for the current iteration.
        iteration_path = os.path.join(FLAGS.output_path,
                                      f'iteration_{iteration + 1}')
        os.mkdir(iteration_path)

        # Generates `num_samples` different configurations.
        noisy_configurations = (
            utilities.coil_configurations.generate_noisy_configurations(
                initial_coefficients=curves_coefficients,
                num_samples=FLAGS.num_samples,
                sigma_scaling_factor=FLAGS.sigma_scaling_factor))

        noisy_objectives = []

        for sample, noisy_configuration in enumerate(noisy_configurations):

            # Create the simsopt coils object for this configuration.
            stellarator_coils = utilities.coils.create_coils(
                curves_coefficients=noisy_configuration,
                coil_currents=coil_currents,
                points_multiplier=FLAGS.points_multiplier,
                num_field_periods=FLAGS.num_field_periods)

            # Create the directory for the current sample.
            sample_path = os.path.join(iteration_path, f'sample_{sample}')
            os.mkdir(sample_path)

            # Saves the coefficients of the base coils to a .npz file.
            np.savez(os.path.join(sample_path, 'coil_coefficients.npz'),
                     *noisy_configuration)

            # Calculates the magnetic field vector and strength.
            magnetic_field = utilities.field.get_magnetic_field_vector(
                plasma_surface=plasma_surface, coils_lst=stellarator_coils)

            magnetic_field_abs = utilities.field.get_magnetic_field_abs(
                plasma_surface=plasma_surface, coils_lst=stellarator_coils)

            # Saves the results to a .npz file.
            np.savez(os.path.join(sample_path, 'field.npz'),
                     magnetic_field=magnetic_field,
                     magnetic_field_absolute=magnetic_field_abs)

            # Get the dictionary with the values of all objectives (including
            # the total objective).
            noisy_objectives.append(
                utilities.objectives.get_all_objectives(
                    plasma_surface=plasma_surface,
                    coils_lst=stellarator_coils,
                    objectives_weights=objectives_weights,
                    num_base_coils=len(curves_coefficients)))

        # Save objective functions to the csv objectives file.
        write_csv_iteration_objectives(csv_filename=objectives_filename,
                                       iteration=iteration,
                                       objectives_lst=noisy_objectives)

        # Create a list with only the total objective.
        total_objective = [
            objectives['total'] for objectives in noisy_objectives
        ]

        # Chooses the configuration with the lowest value of the total
        # objective function.
        curves_coefficients, curves_coefficients_index = (
            utilities.coil_configurations.choose_best_coils_configuration(
                coil_coefficients_set=noisy_configurations,
                objectives_lst=total_objective))

    # Save the results of the best configuration.
    best_configuration_folder_name = 'Final Configuration'
    save_best_configuration(sample_index=curves_coefficients_index,
                            output_path=FLAGS.output_path,
                            folder_name=best_configuration_folder_name,
                            num_iterations=FLAGS.num_iterations)

    # Save the final objectives to a csv folder.
    final_objectives_filename = os.path.join(FLAGS.output_path,
                                             best_configuration_folder_name,
                                             'final_objectives.csv')
    lowest_objective = noisy_objectives[curves_coefficients_index]

    write_csv_header(csv_filename=final_objectives_filename, header=header)
    write_csv_iteration_objectives(csv_filename=final_objectives_filename,
                                   iteration=FLAGS.num_iterations - 1,
                                   objectives_lst=[lowest_objective],
                                   samples=[curves_coefficients_index])


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    app.run(main)

"""FEM linear elastic simulation with FEniCSx."""
#pylint: disable=too-many-function-args

from absl import app
from absl import logging
from absl import flags

import os

import linear_elasticity

FLAGS = flags.FLAGS

# Mesh file flag
flags.DEFINE_string(
    "mesh_path", None,
    "A string representing the path where the mesh file is stored.")

# BC file flag
flags.DEFINE_string(
    "bcs_path", None,
    "A string representing the path where the boundary conditions file is "
    "stored.")

# Material flag
flags.DEFINE_string(
    "material_path", None,
    "A string representing the path where the material file is stored.")

# Mesh flag
flags.DEFINE_string("element_family", "S",
                    "A string representing the mesh element family.")
flags.DEFINE_integer(
    "element_order",
    2,
    "A integer representing the (polynomial) order of the mesh element.",
    lower_bound=1)
flags.DEFINE_enum("quadrature_rule", "gauss_jacobi",
                  ["Default", "gauss_jacobi", "gll", "xiao_gimbutas"],
                  "A string representing the quadrature rule.")

flags.DEFINE_integer("quadrature_degree",
                     2,
                     "A integer representing the quadrature degree.",
                     lower_bound=0)

# Results flag
flags.DEFINE_string(
    "results_dir", None,
    "A string representing the directory where the results file will be stored."
)

SOLVER_OUTPUT_FILENAME = "results.xdmf"
SOLVER_OUTPUT_INFO_FILENAME = "results_info.json"


def main(_):
    solver = linear_elasticity.LinearElasticityFEniCSxSolver(
        FLAGS.element_family, FLAGS.element_order, FLAGS.quadrature_rule,
        FLAGS.quadrature_degree, FLAGS.mesh_path, FLAGS.bcs_path,
        FLAGS.material_path)
    solver.solve()
    results_path = os.path.join(FLAGS.results_dir, SOLVER_OUTPUT_FILENAME)
    solver.save_output(results_path)
    results_info_path = os.path.join(FLAGS.results_dir,
                                     SOLVER_OUTPUT_INFO_FILENAME)
    solver.write_simulation_info_to_json(results_info_path)
    solver.copy_input_files(FLAGS.results_dir)


if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)
    app.run(main)

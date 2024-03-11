"""Utils to define the stress-strain tensors in linear elasticity case."""

from types import FunctionType
from typing import List, Dict, Tuple

import dolfinx
import json
from mpi4py import MPI
import numpy as np
from petsc4py.PETSc import ScalarType
import shutil
import time
import ufl


def get_boundary(boundary_name: str,
                 value_min: float = None,
                 value_max: float = None) -> FunctionType:
    """Gets the boundary condition for a given normal tension at the boundary.

    Args:
        boundary_name: A string representing the name of the region where the
          tension will be applied. The available options are: left, top, right,
          and bottom.
        value_min (float, optional): The minimum value for the boundary 
          condition.
        value_max (float, optional): The maximum value for the boundary
          condition.

    Returns: 
        A boundary condition function that takes a 2D coordinate array 'x' and
          returns a boolean array indicating whether the points satisfy the
          boundary conditions.
    """

    if boundary_name == "left":

        def boundary(x):
            length = max(x[1]) - min(x[1])
            if value_min is None:
                value_min_y = min(x[1])
            else:
                value_min_y = value_min
            if value_max is None:
                value_max_y = max(x[1])
            else:
                value_max_y = value_max
            return (np.logical_and(np.isclose(x[0], min(x[0])), x[1]
                                   >= value_min_y * length, x[1]
                                   <= value_max_y * length))

    elif boundary_name == "bottom":

        def boundary(x):
            width = max(x[0]) - min(x[0])
            if value_min is None:
                value_min_x = min(x[0])
            else:
                value_min_x = value_min
            if value_max is None:
                value_max_x = max(x[0])
            else:
                value_max_x = value_max
            return (np.logical_and(
                np.logical_and(np.isclose(x[1], min(x[1])), x[0]
                               >= value_min_x * width), x[0]
                <= value_max_x * width))

    elif boundary_name == "right":

        def boundary(x):
            length = max(x[1]) - min(x[1])
            if value_min is None:
                value_min_y = min(x[1])
            else:
                value_min_y = value_min
            if value_max is None:
                value_max_y = max(x[1])
            else:
                value_max_y = value_max
            return (np.logical_and(np.isclose(x[0], max(x[0])), x[1]
                                   >= value_min_y * length, x[1]
                                   <= value_max_y * length))

    elif boundary_name == "top":

        def boundary(x):
            width = max(x[0]) - min(x[0])
            if value_min is None:
                value_min_x = min(x[0])
            else:
                value_min_x = value_min
            if value_max is None:
                value_max_x = max(x[0])
            else:
                value_max_x = value_max
            return (np.logical_and(np.isclose(x[1], max(x[1])), x[0]
                                   >= value_min_x * width, x[0]
                                   <= value_max_x * width))

    return boundary


class LinearElasticityStressStrainComputer:
    """Stress and strain computer for a linear elasticity model.

    This class handles linear elasticity, which deals with linearly related
    stress and strain through the constitutive relation of the underlying
    material. The theory of linear elasticity studies elastic solids subjected
    to small deformations, ensuring that the displacements and strains are 
    "linear". This means the components of the displacement field are
    approximately a linear combination of the components of the strain tensor
    of the solid.

    The theory of linear elasticity is only applicable to:
        - Linear elastic solids, where stresses and strains are linearly related
          (material linearity).
        - Small strains, this is the case where strains and displacements are
          linearly related.

    Attributes:
        displacement (dolfinx.fem.function.Function): An instance of the class
          dolfinx.fem.function.Function, representing the displacement u.
        young_modulus (float): Young's modulus of the material.
        poisson_ratio (float, optional): Poisson's ratio of the material.
        convert_2d_to_3d (bool, optional): If true, convert the 2D tensors of
          plane stress or plane strain cases to 3D tensors.
    """

    def __init__(self,
                 displacement: float,
                 young_modulus: float,
                 poisson_ratio: float,
                 convert_2d_to_3d: bool = False) -> None:
        """Initializes a LinearElasticityStressStrainComputer object."""
        self.displacement = displacement
        self.young_modulus = young_modulus
        self.poisson_ratio = poisson_ratio
        self.convert_2d_to_3d = convert_2d_to_3d

        self.shear_modulus = self.young_modulus / (2 * (1 + self.poisson_ratio))
        self.lame_modulus = self.young_modulus * self.poisson_ratio / (
            (1 + self.poisson_ratio) * (1 - 2 * self.poisson_ratio))

    def get_strain_tensor(self):
        """Gets the strain tensor.

        The strain tensor only depends on the displacement field u:
        ε = (1/2) * (∇u + (∇u)^T)

        If the displacement field u is 3D, a 3D strain tensor will be obtained:
        ε = [[ε_xx, ε_xy, ε_xz],
            [ε_xy, ε_yy, ε_yz],
            [ε_xz, ε_yz, ε_zz]]

        If the displacement field u is 2D, a 2D strain tensor will be obtained:
        ε = [[ε_xx, ε_xy],
            [ε_xy, ε_yy]]

        It is possible to convert the 2D strain tensor to 3D in 2D analysis
        through the convert_2d_to_3d parameter, adding the z strain 
        components.

        In the plane strain case, all z components of the strain are zero.
        The same happens in the plane stress state, except the ε_zz component
        that is non-zero:
        ε_zz = -(λ / (λ + 2μ)) * (ε_xx + ε_yy)
        """

        strain = 0.5 * (ufl.nabla_grad(self.displacement) +
                        ufl.nabla_grad(self.displacement).T)

        if self.convert_2d_to_3d:
            strain_zz = -self.lame_modulus / (
                self.lame_modulus + 2 * self.shear_modulus) * (strain[0, 0] +
                                                               strain[1, 1])
            strain = ufl.as_tensor([[strain[0, 0], strain[0, 1], 0],
                                    [strain[1, 0], strain[1, 1], 0],
                                    [0, 0, strain_zz]])

        return strain

    def get_stress_tensor(self):
        """Gets the stress tensor.

        The stress tensor is defined as:
        σ = λ * tr(ε) * I + 2μ * ε

        If it is a plane stress state, it is necessary to change the λ to
        λ^*:
        σ = λ^* * tr(ε) * I + 2μ * ε

        where λ^* = 2λμ / (λ + 2μ) and tr(ε) = ∇ · u.

        If the displacement field u is 3D, a 3D stress tensor will be obtained:
        ε = [[σ_xx, σ_xy, σ_xz],
            [σ_xy, σ_yy, σ_yz],
            [σ_xz, σ_yz, σ_zz]]

        If the displacement field u is 2D, a 2D stress tensor will be obtained:
        ε = [[σ_xx, σ_xy],
            [σ_xy, σ_yy]]

        It is possible to convert the 2D strain tensor to 3D for 2D analysis
        through the convert_2d_to_3d parameter, adding the z stress 
        components.

        In the plane stress case, all z components of the stress are zero.
        The same happens in the plane strain state, except the σ_zz component
          is different from zero:
        σ_zz = λ * (ε_xx + ε_yy)
        """

        lame_modulus = 2 * self.lame_modulus * \
            self.shear_modulus / (
                self.lame_modulus +
                2 * self.shear_modulus)

        dim = len(self.displacement)
        strain = 0.5 * (ufl.nabla_grad(self.displacement) +
                        ufl.nabla_grad(self.displacement).T)
        stress = lame_modulus * ufl.nabla_div(self.displacement) * \
            ufl.Identity(dim) + \
            2 * self.shear_modulus \
            * strain

        if self.convert_2d_to_3d:
            stress = ufl.as_tensor([[stress[0, 0], stress[0, 1], 0],
                                    [stress[1, 0], stress[1, 1], 0], [0, 0, 0]])

        return stress

    def get_von_mises_stress(self):
        """Gets von Mises stress.

        The von Mises stress is given by:
        σ_m = √(3/2 * s:s)

        where s:
        s = σ - (1/3) * tr(σ) * I

        σ is the stress tensor, tr(σ) is the trace of σ, and I is the identity 
        tensor.

        If the case is 2D or 3D the space dimension will be the same as the
        displacement dimension.

        However, if we want to convert 2D stress and strain tensors to 3d
        tensors, we will have to add 1 dimension to the 2D displacement
        dimension.
        """
        # Space dimension
        if self.convert_2d_to_3d:
            d = len(self.displacement) + 1
        else:
            d = len(self.displacement)

        # Deviatoric stress
        deviatoric_stress = self.get_stress_tensor() - (1. / 3) * ufl.tr(
            self.get_stress_tensor()) * ufl.Identity(d)

        # von Mises stress
        von_mises_stress = ufl.sqrt(
            3. / 2 * ufl.inner(deviatoric_stress, deviatoric_stress))

        return von_mises_stress


class LinearElasticityFEniCSxSolver:
    """Linear elasticity solver in FEniCSx.

    The linear elasticity case is made up of a mesh, boundary conditions,
    and a material.

    To solve the model through variational formulation in FEniCSx, we will use
    the "solve" function. With this function, we obtain the displacements for
    each node of the mesh. Using the displacements and the constitutive laws of
    linear elasticity, we calculate the stress and strain fields 
    through the "save_output" function.

    Attributes:
        element_family (str): The type of mesh element family.
        element_order (int): An integer representing the (polynomial) order of
          the mesh element.
        quadrature_rule (str): A string representing the mesh quadrature rule.
        quadrature_degree (int): An integer representing the quadrature degree.
        mesh_path (str): A path where the mesh file is stored.
        bcs_path (str): A path where the BCs file are stored.
        material_path (str): A path where the material file is stored.
        dolfinx_mesh (dolfinx.cpp.mesh.Mesh): An instance of the
          "dolfinx.cpp.mesh.Mesh" class, representing the FEniCSx mesh.
        displacement_dict_list (list): A list of dictionaries containing the
          displacement boundary conditions data.
        tension_dict_list (list): A list of dictionaries containing the
          tension boundary conditions data.
        v_func_space (dolfinx.fem.FunctionSpace): An instance of the
          "dolfinx.fem.FunctionSpace" class, representing the finite element
          function space.
        u_trial_func (ufl.argument.Argument): An instance of the
          "ufl.argument.Argument" class, representing the trial function.
        v_test_func (ufl.argument.Argument): An instance of the
          "ufl.argument.Argument" class, representing the test function.
        displacement_func (dolfinx.fem.Function): An instance of the
          "dolfinx.fem.Function" class, representing the displacement field.
        stress_func (dolfinx.fem.Function): An instance of the
          "dolfinx.fem.Function" class, representing the stress field.
        strain_func (dolfinx.fem.Function): An instance of the
          "dolfinx.fem.Function" class, representing the strain field.
        von_mises_func (dolfinx.fem.Function): An instance of the
          "dolfinx.fem.Function" class, representing the Von Mises stress
          field.
        runtime (float): A float representing the runtime of the simulation.
    """

    def __init__(self, element_family: str, element_order: int,
                 quadrature_rule: str, quadrature_degree: int, mesh_path: str,
                 bcs_path: str, material_path: str) -> None:
        """Initializes a LinearElasticityFEniCSxSolver object."""
        self.element_family = element_family
        self.element_order = element_order
        self.quadrature_rule = quadrature_rule
        self.quadrature_degree = quadrature_degree
        self.mesh_path = mesh_path
        self.bcs_path = bcs_path
        self.material_path = material_path

        self.dolfinx_mesh = self._load_mesh()
        self.young_modulus, self.poisson_ratio = self._load_material_data()
        self.displacement_dict_list, self.tension_dict_list = (
            self._load_bc_data())

        self.v_func_space = None
        self.u_trial_func = None
        self.v_test_func = None

        self.displacement_func = None
        self.stress_func = None
        self.strain_func = None
        self.von_mises_func = None

        self.runtime = 0

    def _load_material_data(self) -> Tuple[float, float]:
        """Loads material data from a JSON.

        Loads the Young modulus and Poisson ratio of a material from a JSON
        file. The JSON file is expected to contain the keys "young_modulus" and
        "poisson_ratio".

        Returns:
            A tuple containing young_modulus (float) and poisson_ratio (float).

        Raises:
            KeyError: If the JSON file does not contain "young_modulus" or 
              "poisson_ratio" keys.

        Returns:
            A tuple containing "young_modulus" (float) and "poisson_ratio" 
              (float) read from the JSON file.
        """
        with open(self.material_path, "r", encoding="utf-8") as read_file:
            material_dict = json.load(read_file)

        try:
            young_modulus = material_dict["young_modulus"]
            poisson_ratio = material_dict["poisson_ratio"]
        except KeyError as exc:
            raise KeyError("JSON file does not contain 'young_modulus' or "
                           "'poisson_ratio' keys.") from exc

        return young_modulus, poisson_ratio

    def _load_mesh(self) -> dolfinx.mesh:
        """Loads a mesh from an MSH file and returns the DOLFINx mesh object.

        Returns:
            dolfinx_mesh (dolfinx.Mesh): The DOLFINx mesh object.
        """
        dolfinx_mesh, _, _ = dolfinx.io.gmshio.read_from_msh(self.mesh_path,
                                                             MPI.COMM_WORLD,
                                                             gdim=2)

        return dolfinx_mesh

    def _load_bc_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Loads boundary condition data from a JSON file.

        Loads the Dirichlet and Neumann boundary conditions from a JSON file. 
        The JSON file is expected to contain the keys: "displacement" and 
        "tension". The "displacement" key corresponds to an array of
        dictionaries, each representing a Dirichlet boundary condition. 

        Each Dirichlet boundary condition has three properties: "boundary_name", 
        "displacement_x", and "displacement_y". The "boundary_name" property
        denotes the name of the boundary to which the condition is applied,
        and "displacement_x" and "displacement_y" represent the displacements
        in the x and y directions, respectively.

        Similarly, the "tension" key also corresponds to an array of
        dictionaries, each representing a Neumann boundary condition. Each
        Neumann boundary condition has three properties: "boundary_name",
        "tension_x", and "tension_y". The "boundary_name" property indicates
        the name of the boundary where the condition is applied, and 
        "tension_x" and "tension_y" represent the tension or force components
        in the x and y directions, respectively.

        Both of them are expressed as percentages, with "boundary_start"
        indicating where the boundary condition starts and "boundary_end"
        indicating where it finishes being applied on the boundary.

        Returns:
            A tuple containing displacement_dict_list (list of dictionaries) and 
                tension_dict_list (list of dictionaries).

         Raises:
            KeyError: If the JSON file does not contain the required keys.
        """
        with open(self.bcs_path, "r", encoding="utf-8") as read_file:
            bcs_dict = json.load(read_file)

        try:
            displacement_dict_list = bcs_dict["displacement"]
            tension_dict_list = bcs_dict["tension"]
        except KeyError as exc:
            raise KeyError(
                f"Required keys not found in JSON file: {str(exc)}") from exc

        return displacement_dict_list, tension_dict_list

    def _get_bilinear_form_a(self) -> ufl.form.Form:
        """Gets the bilinear form a(u, v) in FEniCSx.

        The bilinear form is defined as:
        a(u, v) = ∫Ω σ(u) : ε(v) dx

        where:
            - σ is the stress tensor.
            - ε is the strain tensor.
            - colon operator (:) is the inner product between tensors.
            - dx represents the differential element for integration over the 
              domain Ω.

        Returns:
            bilinear_form_a (ufl.form.Form): The bilinear form a(u, v), where u
              is the trial function and v is the test function.
        """

        # Compute the stress tensor for the trial function
        stress_u = LinearElasticityStressStrainComputer(
            displacement=self.u_trial_func,
            young_modulus=self.young_modulus,
            poisson_ratio=self.poisson_ratio).get_stress_tensor()

        # Compute the strain tensor for the test function
        strain_v = LinearElasticityStressStrainComputer(
            displacement=self.v_test_func,
            young_modulus=self.young_modulus,
            poisson_ratio=self.poisson_ratio).get_strain_tensor()

        # Compute the bilinear form a(u, v) = σ(u) : ε(v) * dx
        bilinear_form_a = ufl.inner(stress_u, strain_v) * ufl.dx(
            metadata={
                "quadrature_degree": self.quadrature_degree,
                "quadrature_rule": self.quadrature_rule
            })

        return bilinear_form_a

    def _get_linear_form_l(self) -> ufl.form.Form:
        """Gets the linear form L(v) for the variational formulation in FEniCSx.

        The linear form is defined as:
        L(v) = ∫Ω f · v dx + ∫∂ΩT · v ds

        where:
            - f is body forces.
            - T is the traction or stress vector at the boundary.
            - dx represents the differential element for integration over the 
              domain Ω.
            - ds represents the differential element for integration over the 
              boundary ∂.

        We assume the body forces f are zero: L(v) = ∫∂ΩT · v ds.
        Note that the linear_form_l will split into integrals over the boundary 
        parts.

        The integral over each boundary part will only be considered if that 
        boundary is being pulled.

        Returns:
            linear_form_l (ufl.form.Form): The linear form L(v), where v is the
              test fucntion.
        """

        facet_indices = []
        facet_markers = []

        # Dimension of facets in the mesh
        facet_dim = self.dolfinx_mesh.topology.dim - 1

        # Get facet indices and markers for each boundary of the tension
        # object
        for i, tension_dict in enumerate(self.tension_dict_list):

            # Get the boundary info for the tension object
            boundary_name = tension_dict["boundary_name"]
            boundary_start = tension_dict["boundary_start"]
            boundary_end = tension_dict["boundary_end"]

            # Get a boundary function
            boundary = get_boundary(boundary_name, boundary_start, boundary_end)

            # Obtain the indices of the facets
            facet_indices_boundary = dolfinx.mesh.locate_entities_boundary(
                self.dolfinx_mesh, facet_dim, boundary)

            facet_indices.append(facet_indices_boundary)
            facet_markers.append(np.full_like(facet_indices_boundary, i))

        # Combine the facet indices and markers into numpy arrays
        facet_indices = np.hstack(facet_indices).astype(np.int32)
        facet_markers = np.hstack(facet_markers).astype(np.int32)

        # Sort the facets based on the indices
        sorted_facets = np.argsort(facet_indices)

        # Create facet tags for integration over boundaries
        facet_tag = dolfinx.mesh.meshtags(self.dolfinx_mesh, facet_dim,
                                          facet_indices[sorted_facets],
                                          facet_markers[sorted_facets])

        # Define the measure for integration over boundaries
        ds = ufl.Measure("ds",
                         domain=self.dolfinx_mesh,
                         subdomain_data=facet_tag)

        # Convert tension boundary conditions to FEniCSx form
        tension_fenicsx_list = self._convert_tension_bc_to_fenicsx()

        # Iterate over tension and add terms to the linear form
        linear_form_l = 0
        for i, tension in enumerate(tension_fenicsx_list):
            linear_form_l += ufl.dot(tension, self.v_test_func) * ds(
                i,
                metadata={
                    "quadrature_degree": self.quadrature_degree,
                    "quadrature_rule": self.quadrature_rule
                })

        return linear_form_l

    def _convert_tension_bc_to_fenicsx(self) -> List[dolfinx.fem.Constant]:
        """Converts the tension boundary conditions to FEniCSx objects.

        Returns:
            tension_fenicsx_list (list): A list of FEniCSx Constant objects
              representing the tension boundary conditions.
        """

        tension_fenicsx_list = []

        # Loop through each tension boundary condition object
        for tension_dict in self.tension_dict_list:

            # Create a FEniCSx Constant object with the tension values
            tension = dolfinx.fem.Constant(
                self.dolfinx_mesh,
                ScalarType(
                    (tension_dict["tension_x"], tension_dict["tension_y"])))

            tension_fenicsx_list.append(tension)

        return tension_fenicsx_list

    def _convert_displacement_bc_to_fenicsx(
            self) -> List[dolfinx.fem.dirichletbc]:
        """Converts the displacement boundary conditions objects to FEniCSx.

        Returns:
            displacement_fenicsx_list (list): A list of FEniCSx DirichletBC
              objects representing the displacement boundary conditions.
        """

        displacement_fenicsx_list = []

        # Iterate through all displacement objects
        for displacement_dict in self.displacement_dict_list:

            # Get the boundary info for the displacement object
            boundary_name = displacement_dict["boundary_name"]
            boundary_start = displacement_dict["boundary_start"]
            boundary_end = displacement_dict["boundary_end"]

            # Get a boundary function
            boundary = get_boundary(boundary_name, boundary_start, boundary_end)

            # Displacement in x
            if displacement_dict["displacement_x"] is not None:

                # Obtain subspace from the function space
                sub_0, _ = self.v_func_space.sub(0).collapse()

                # Identify boundary edges in the mesh
                edges = dolfinx.mesh.locate_entities_boundary(
                    self.dolfinx_mesh, self.dolfinx_mesh.topology.dim - 1,
                    boundary)

                # Locate boundary DOFs for applying boundary conditions
                boundary_dofs = dolfinx.fem.locate_dofs_topological(
                    (self.v_func_space.sub(0), sub_0),
                    self.dolfinx_mesh.topology.dim - 1, edges)

                # Create a displacement function for the subdomain 'sub_0'
                disp_func = dolfinx.fem.Function(sub_0)

                # Define a constant for displacement boundary condition value
                # for x-displacement
                x_disp_const = dolfinx.fem.Constant(
                    self.dolfinx_mesh,
                    ScalarType(displacement_dict["displacement_x"]))

                # Create an expression for x-displacement and interpolate onto
                # the displacement function
                x_disp_expr = dolfinx.fem.Expression(
                    x_disp_const, sub_0.element.interpolation_points())
                disp_func.interpolate(x_disp_expr)

                # Create a displacement boundary condition using the
                # displacement function
                bc = dolfinx.fem.dirichletbc(disp_func, boundary_dofs,
                                             self.v_func_space.sub(0))

                displacement_fenicsx_list.append(bc)

            # Displacement in y
            if displacement_dict["displacement_y"] is not None:

                # Obtain subspace from the function space
                sub_1, _ = self.v_func_space.sub(1).collapse()

                # Identify boundary edges in the mesh
                edges = dolfinx.mesh.locate_entities_boundary(
                    self.dolfinx_mesh, self.dolfinx_mesh.topology.dim - 1,
                    boundary)

                # Locate boundary DOFs for applying boundary conditions
                boundary_dofs = dolfinx.fem.locate_dofs_topological(
                    (self.v_func_space.sub(1), sub_1),
                    self.dolfinx_mesh.topology.dim - 1, edges)

                # Create a displacement function for the subdomain 'sub_1'
                disp_func = dolfinx.fem.Function(sub_1)

                # Define a constant for displacement boundary condition value
                # for y-displacement
                y_disp_const = dolfinx.fem.Constant(
                    self.dolfinx_mesh,
                    ScalarType(displacement_dict["displacement_y"]))

                # Create an expression for y-displacement and interpolate onto
                # the displacement function
                y_disp_expr = dolfinx.fem.Expression(
                    y_disp_const, sub_1.element.interpolation_points())
                disp_func.interpolate(y_disp_expr)

                # Create a displacement boundary condition using the
                # displacement function
                bc = dolfinx.fem.dirichletbc(disp_func, boundary_dofs,
                                             self.v_func_space.sub(1))

                displacement_fenicsx_list.append(bc)

        return displacement_fenicsx_list

    def _compute_stress_field(self) -> dolfinx.fem.function.Function:
        """Compute the stress field from the displacement field.

        Returns:
            field (dolfinx.fem.function.Function): The computed field.
        """
        # Create the function space for stress
        v_func_space = dolfinx.fem.TensorFunctionSpace(
            self.dolfinx_mesh, (self.element_family, self.element_order),
            shape=(3, 3))

        # Compute the stress tensor
        tensor = LinearElasticityStressStrainComputer(
            displacement=self.displacement_func,
            young_modulus=self.young_modulus,
            poisson_ratio=self.poisson_ratio,
            convert_2d_to_3d=True).get_stress_tensor()

        return self._interpolate_expression_to_field(tensor, v_func_space)

    def _compute_strain_field(self) -> dolfinx.fem.function.Function:
        """Compute the strain field.

        Returns:
            field (dolfinx.fem.function.Function): The computed field.
        """
        # Create the function space for strain
        v_func_space = dolfinx.fem.TensorFunctionSpace(
            self.dolfinx_mesh, (self.element_family, self.element_order),
            shape=(3, 3))

        # Compute the strain tensor
        tensor = LinearElasticityStressStrainComputer(
            displacement=self.displacement_func,
            young_modulus=self.young_modulus,
            poisson_ratio=self.poisson_ratio,
            convert_2d_to_3d=True).get_strain_tensor()

        return self._interpolate_expression_to_field(tensor, v_func_space)

    def _compute_von_mises_stress_field(self) -> dolfinx.fem.function.Function:
        """Compute the von Mises stress field from the displacement field.

        Returns:
            field (dolfinx.fem.function.Function): The computed field.
        """
        # Create the function space for von Mises stress
        v_func_space = dolfinx.fem.FunctionSpace(
            self.dolfinx_mesh, (self.element_family, self.element_order))

        # Compute the von Mises stress
        tensor = LinearElasticityStressStrainComputer(
            displacement=self.displacement_func,
            young_modulus=self.young_modulus,
            poisson_ratio=self.poisson_ratio,
            convert_2d_to_3d=True).get_von_mises_stress()

        return self._interpolate_expression_to_field(tensor, v_func_space)

    def _interpolate_expression_to_field(
        self, tensor: list, v_func_space: dolfinx.fem.FunctionSpace
    ) -> dolfinx.fem.function.Function:
        """Interpolates the given tensor expression to obtain a field.

        Args:
            tensor (callable or list): The expression to be interpolated.
            v_func_space (dolfinx.fem.FunctionSpace): The function space to 
              interpolate the expression.

        Returns:
            dolfinx.fem.Function: The interpolated field.
        """
        # Create the expression for the field
        field_expr = dolfinx.fem.Expression(
            tensor, v_func_space.element.interpolation_points())

        # Interpolate the expression to obtain the field
        field = dolfinx.fem.Function(v_func_space)
        field.interpolate(field_expr)

        return field

    def _compute_stress_strain_fields(self):
        """Compute stress, strain, and von Mises stress fields."""
        self.stress_func = self._compute_stress_field()
        self.strain_func = self._compute_strain_field()
        self.von_mises_func = self._compute_von_mises_stress_field()

    def write_output_fields_to_xdmf(self, results_path) -> None:
        """Writes output fields to an XDMF file.

        Args:
            results_path (str): A path where the results file will be stored.
        """

        # Create a dictionary of fields to write
        fields = {
            "displacement": self.displacement_func,
            "stress": self.stress_func,
            "strain": self.strain_func,
            "von_mises": self.von_mises_func
        }

        # Write all the fields to the file
        with dolfinx.io.XDMFFile(self.dolfinx_mesh.comm, results_path,
                                 "w") as xdmf:
            xdmf.write_mesh(self.dolfinx_mesh)

            for field_name, field in fields.items():
                field.name = field_name
                xdmf.write_function(field)

    def write_simulation_info_to_json(self, json_path: str) -> None:
        """Write simulation information to a JSON file.

        Args:
            json_path (str): The simulation information file path in JSON
              format.
        """

        # Create a dictionary with mesh information
        simulation_info_dict = {
            "element family": self.element_family,
            "element order": self.element_order,
            "quadrature rule": self.quadrature_rule,
            "quadrature degree": self.quadrature_degree,
            "runtime (s)": self.runtime
        }

        # Write the mesh info to JSON file
        with open(json_path, "w", encoding="utf-8") as write_file:
            json.dump(simulation_info_dict, write_file, indent=4)

    def solve(self):
        """Solves the model through variational formulation in FEniCSx.

        The steps to solve the variational formulation are:
            0. We have a PDE: −∇⋅σ = f
            1. We then choose a test function v and multiply both sides of the
            above equation and integrate over all test functions:
            −∫Ω (∇⋅σ)⋅v dx = ∫Ω f⋅v dx
            2. Define the bilinear form: a(u, v) = ∫Ω σ(u) : ε(v) dx
            3. Define the linear form: L(v) = ∫∂Ω T · v ds
            4. Solve the variational formulation: a(u, v) = L(v)

        To solve the variational formulation, it is necessary to provide a list
        of Dirichlet boundary conditions. This list is obtained through the
        _convert_displacement_bc_to_fenicsx() function.
        """

        # 1. Define trial and test function
        self.v_func_space = dolfinx.fem.VectorFunctionSpace(
            self.dolfinx_mesh, (self.element_family, self.element_order))
        self.u_trial_func = ufl.TrialFunction(self.v_func_space)
        self.v_test_func = ufl.TestFunction(self.v_func_space)

        # 2. Define bilinear form
        bilinear_form_a = self._get_bilinear_form_a()

        # 3. Define linear form
        linear_form_l = self._get_linear_form_l()

        # 4. Solve the variational formulation
        linear_variational_problem = dolfinx.fem.petsc.LinearProblem(
            a=bilinear_form_a,
            L=linear_form_l,
            bcs=self._convert_displacement_bc_to_fenicsx(),
            petsc_options={
                "ksp_type": "preonly",
                "pc_type": "lu"
            })

        start = time.time()
        self.displacement_func = linear_variational_problem.solve()
        end = time.time()
        self.runtime = np.round(end - start, 3)

    def save_output(self, results_path):
        """Calculates fields and writes results to an XDMF file.

        Args:
            results_path (str): A path where the results file will be stored.
        """
        # 1. Computes stress and strain fields
        self._compute_stress_strain_fields()

        # 2. Writes results to an XDMF file
        self.write_output_fields_to_xdmf(results_path)

    def copy_input_files(self, destination_path):
        """Copy input files to a destination path.

        Args:
            destination_path (str): The destination path for copying the input 
              files.
        """
        input_file_paths = [self.mesh_path, self.bcs_path, self.material_path]

        for file_path in input_file_paths:
            shutil.copy(file_path, destination_path)

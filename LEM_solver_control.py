import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import Nodes
import Elements
import LEM_solver_routine
import LEM_output

def time_solver(parameters):

    nodes, elements, boundary, bd_cond, control_parameters = parameters
    dt, t_total, output_cycle = control_parameters
    print parameters

    for t in range(t_total):
        LEM_solver_routine.set_displacement_boundary_condition(t, parameters)
        LEM_solver_routine.set_node_position()
        LEM_solver_routine.set_velocity_half_time_step()
        LEM_solver_routine.init_forces_and_stats_variables()
        LEM_solver_routine.force_in_elements()
        LEM_solver_routine.classify_broken_and_unbroken_elements()
        LEM_solver_routine.nodes_acceleration()
        LEM_solver_routine.set_spheres_from_broken_elements()

        if t % output_cycle == 0:
            LEM_output.draw_nodes(nodes, boundary)

        LEM_solver_routine.sphere_normal_contact()

        LEM_solver_routine.set_forces_boundary_condition()
        LEM_solver_routine.set_acceleration()
        LEM_solver_routine.set_velocity()

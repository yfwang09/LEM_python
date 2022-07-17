import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt

import Nodes
import Elements
import LEM_solver_routine
import LEM_output

def time_solver(parameters):

    nodes, elements, boundary, bd_cond, control_parameters = parameters
    dt, t_total, output_cycle = control_parameters
    print (parameters)

    for t in range(t_total):
        LEM_solver_routine.set_displacement_boundary_condition(t, parameters)
        """
        u0 = np.array([])
        for i in range(nodes.n):
            u0 = np.append(u0, nodes.pos(i))
        res = sp.optimize.minimize(LEM_solver_routine.PotentialEnergy, u0, args=(t, parameters))

        """
        LEM_solver_routine.set_node_position(nodes, dt)
        LEM_solver_routine.set_velocity_half_time_step(nodes, dt)
        LEM_solver_routine.init_forces_and_stats_variables(nodes)
        LEM_solver_routine.force_in_elements(elements)
        LEM_solver_routine.classify_broken_and_unbroken_elements()
        LEM_solver_routine.nodes_acceleration(nodes, elements)
        LEM_solver_routine.set_spheres_from_broken_elements()
        
        if t % (output_cycle) == 0:
            LEM_output.draw_nodes(nodes, boundary)
        if t % 100 == 0:
            print ('time step: ' + str(t))
            print ('max velocity: ' + str(nodes.v(8)))#str(np.max(nodes._v))
            for i in range(nodes.n):
                x_i = nodes.pos(i)
                v_i = nodes.v(i)
                plt.plot([x_i[0], x_i[0]+10*v_i[0]],[x_i[1], x_i[1]+10*v_i[1]])
        
        LEM_solver_routine.sphere_normal_contact()

        LEM_solver_routine.set_forces_boundary_condition()
        LEM_solver_routine.set_acceleration()
        LEM_solver_routine.set_velocity(dt, nodes)
        
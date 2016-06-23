import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import Nodes
import Elements

def set_displacement_boundary_condition(t, parameters):
    nodes, elements, boundary, bd_cond, control_parameters = parameters
    dt, t_total, output_cycle = control_parameters
    for bc in bd_cond:
        bd_face, start, end, disp = bc
        disp = np.array([0, disp, 0])   # displacement only on y direction
        if end == -1:
            end = t_total
        if start <= t < end:
            #print t, bd_face
            bd_nodes = boundary[bd_face]
            #print nodes.pos_list()[1][bd_nodes]
            for i in bd_nodes:
                #print nodes.pos(i), disp, nodes.pos(i)+disp
                nodes.posIs(i, nodes.pos(i) + disp)
                nodes.vIs(i, 0)
                nodes.aIs(i, 0)
                #print nodes.pos(i)
            #print nodes.pos_list()[1][bd_nodes]

def set_node_position():
    pass

def set_velocity_half_time_step():
    pass

def init_forces_and_stats_variables():
    pass

def force_in_elements():
    pass

def classify_broken_and_unbroken_elements():
    pass

def nodes_acceleration():
    pass

def set_spheres_from_broken_elements():
    pass

def sphere_normal_contact():
    pass

def set_forces_boundary_condition():
    pass

def set_acceleration():
    pass

def set_velocity():
    pass

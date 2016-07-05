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

def is_bd_node(boundary, i):
    for bd_face in boundary:
        if i in boundary[bd_face]:
            return True
    return False

def PotentialEnergy(u, t, parameters):
    nodes, elements, boundary, bd_cond, control_parameters = parameters
    U = 0
    for i in range(nodes.n):
        if is_bd_node(boundary, i):
            nodes.posIs(i, np.array([u[i*3], 0, u[i*3+2]]))
        else:
            nodes.posIs(i, u[i*3:i*3+3])
    for i in range(elements.n):
        U += elements.Ue(i)
    return U

def set_node_position(nodes, dt):
    for i in range(nodes.n):
        new_x = nodes.pos(i) + dt * nodes.v(i) + 0.5 * (dt**2) * nodes.a(i)
        nodes.posIs(i, new_x)

def set_velocity_half_time_step(nodes, dt):
    for i in range(nodes.n):
        new_v = nodes.v(i) + 0.5 * dt * nodes.a(i)
        nodes.vIs(i, new_v)

def init_forces_and_stats_variables(nodes):
    for i in range(nodes.n):
        nodes.aIs(i, 0)

def force_in_elements(elems):
    pass

def classify_broken_and_unbroken_elements():
    pass

def nodes_acceleration(nodes, elements):
    for k in range(elements.n):
        f_k = elements.f(k)
        n_vec = np.array([np.cos(elements.theta0[k]), np.sin(elements.theta0[k]), 1])
        i = elements._conn[k][0]
        j = elements._conn[k][1]
        a_i = nodes.a(i)
        a_j = nodes.a(j)
        nodes.aIs(i, a_i + f_k[:3])
        nodes.aIs(j, a_j + f_k[-3:])
    # damping
    for i in range(nodes.n):
        v_i = nodes.v(i)
        a_i = nodes.a(i)
        nodes.aIs(i, a_i - 0.2*v_i)

def set_spheres_from_broken_elements():
    pass

def sphere_normal_contact():
    pass

def set_forces_boundary_condition():
    pass

def set_acceleration():
    # mass of node = 1
    pass

def set_velocity(dt, nodes):
    for i in range(nodes.n):
        nodes.vIs(i, nodes.v(i) + 0.5*dt*nodes.a(i))


import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import Nodes
import Elements
import LEM_solver_routine
import LEM_output

def time_solver(nodes, elements, boundary):
    
    LEM_solver_routine.set_displacement_boundary_condition()
    LEM_solver_routine.set_node_position()
    LEM_solver_routine.set_velocity_half_time_step()
    LEM_solver_routine.init_forces_and_stats_variables()

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import Nodes
import Elements

def draw_nodes(nodes, boundary):
    plt.figure()
    node_x, node_y, node_phi = nodes.pos_list()
    plt.plot(node_x, node_y, 'o')
    for bd_face in boundary:
        node_index = boundary[bd_face]
        plt.plot(node_x[node_index], node_y[node_index], 'go')

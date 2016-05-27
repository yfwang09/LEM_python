import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import Nodes
import Elements

def read_nodes(f):
    n_nodes = int(f.readline())
    nodes = Nodes.Nodes(n_nodes)
    for i in range(n_nodes):
        line = f.readline()
        line_split = line.split()
        nid = i
        mat = line_split[1]
        x0 = (float(line_split[2]), float(line_split[3]))
        nodes.nodeIs(nid, x0, mat)
    return nodes

def read_elements(f, nodes):
    n_elements = int(f.readline())
    elements = Elements.Elements(n_elements, nodes)
    for i in range(n_elements):
        line = f.readline()
        line_split = line.split()
        nid = i
        node_i = int(line_split[1])
        node_j = int(line_split[2])
        interface = line_split[3]
        elements.elementIs(nid, node_i, node_j, interface)
    return elements

def read_boundary(f, nodes):
    n_boundary = int(f.readline())
    boundary = {}
    for i in range(n_boundary):
        bd_name = f.readline().split()[0]
        n_bd_nodes = int(f.readline().split()[0])
        bd_nodes = np.array([False] * nodes.n)
        for j in range(n_bd_nodes):
            bd_nodes[int(f.readline().split()[0])] = True
        boundary[bd_name] = bd_nodes
    return boundary

def read_inputs():
    print 'reading input files...'
    nodes = ''; elements = ''; boundary = '';

    with open('input_file.txt', 'r') as f:
        for line in iter(f.readline, ''):
            print line[:-1]
            if line[0] == '#' or line[0] == '\n':
                continue
            if line.split()[0] == 'NODE':
                nodes = read_nodes(f)
            elif line.split()[0] == 'ELEMENT':
                elements = read_elements(f, nodes)
            elif line.split()[0] == 'BOUNDARY':
                boundary = read_boundary(f, nodes)
            else:
                print 'input file form error'
                break

    return (nodes, elements, boundary)

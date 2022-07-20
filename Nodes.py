import numpy as np
import matplotlib.pyplot as plt

class Nodes:
    def __init__(self, nx=6, ny=None, crack=(0, -1)):
        self.nx = nx
        self.ny = nx if ny is None else ny
        self.create_triangle_lattice(self.nx, self.ny, crack)

    def create_triangle_lattice(self, nx, ny, crack):
        x = []
        y = []
        dy = np.sqrt(3)/2 # distance per layer
        self.n = 0
        
        # Initialize x, y coordinates of the nodes
        for i in range(ny):
            # n_per_layer = nx if i%2 == 0 else nx + 1
            n_per_layer = nx
            if i % 2 == 0:
                x.append(np.arange(n_per_layer))
            else:
                x.append(np.arange(n_per_layer) + 0.5)
            self.n += n_per_layer
            y.append(np.ones(n_per_layer) * i * dy)
        x = np.concatenate(x)
        y = np.concatenate(y)
        z = np.zeros(self.n)
        self.u0 = np.vstack((x, y, z)).transpose()
        self.u = np.vstack((x, y, z)).transpose()

        # Create neighbor list of nodes
        self.conn = []
        possible_next_node = [-1, 1, -nx-1, -nx, -nx+1, nx-1, nx, nx+1] # cell list
        for i in range(self.n):
            conn_ = []
            for next in possible_next_node:
                if i + next < 0 or i + next >= self.n: continue
                # remove the bonds to create a crack (y, a)
                if (np.minimum(y[i], y[i+next]) < crack[0] and 
                    np.maximum(y[i], y[i+next]) > crack[0] and
                    0.5*(x[i] + x[i+next]) < crack[1]
                   ):
                    continue
                if np.linalg.norm(self.u0[i] - self.u0[i + next]) < 1.1:
                    conn_.append(i + next)
            self.conn.append(conn_)

    def pos(self, i):
        return self.u[i]

    def posIs(self, i, u):
        self.u[i] = u

    def displacement (self, k):
        return self.u[k][:] - self.u0[k][:]

    def visualize2D(self, figax=None, show=True, color='ok', bc_node_index=None, bc_color='^k'):
        if figax is None:
            figax = plt.subplots()
        _, ax = figax
        if bc_node_index is None: bc_node_index = np.zeros(self.n, dtype=bool)
        ax.plot(self.u[bc_node_index, 0], self.u[bc_node_index, 1], bc_color)
        ax.plot(self.u[np.logical_not(bc_node_index), 0], self.u[np.logical_not(bc_node_index), 1], color)
        if show: plt.show()

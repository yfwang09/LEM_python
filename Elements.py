import numpy as np
import matplotlib.pyplot as plt

class Elements:
    def __init__(self, node_):
        self.node_ = node_
        self.create_elements()

    def create_elements(self):
        self.edge = []
        node_ = self.node_
        node_.elem = [[] for _ in range(node_.n)]
        for i in range(node_.n):
            for j in node_.conn[i]:
                if i < j:
                    self.edge.append((i, j))
                    elem_id = len(self.edge) - 1
                    node_.elem[i].append(elem_id)
                    node_.elem[j].append(elem_id)
        self.edge = np.array(self.edge, dtype=int)
        self.n = len(self.edge)
        self.l0 = np.ones(self.n)
        self.K = np.ones(self.n)

    def U_pot(self, u, dof_index=None):
        uval = self.node_.u.copy()
        if dof_index is None: dof_index = np.ones_like(uval, dtype=bool)
        uval[dof_index] = u
        ui = uval[self.edge[:, 0]]
        uj = uval[self.edge[:, 1]]
        l = np.linalg.norm(uj - ui, axis=1)
        Ue = self.K*(l - self.l0)**2
        return np.sum(Ue)

    def visualize2D(self, figax=None, show=True, color=':C0', bc_edge_index=None, bc_color='k'):
        if figax is None:
            figax = plt.subplots()
        _, ax = figax
        if bc_edge_index is None: bc_edge_index = np.zeros(self.n, dtype=bool)
        for i in range(self.n):
            xval = [self.node_.u[self.edge[i][0], 0], self.node_.u[self.edge[i][1], 0]]
            yval = [self.node_.u[self.edge[i][0], 1], self.node_.u[self.edge[i][1], 1]]
            if bc_edge_index[i]:
                ax.plot(xval, yval, bc_color)
            else:
                ax.plot(xval, yval, color)
        if show: plt.show()

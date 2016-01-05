import numpy as np

class Nodes:
    def __init__(self):
        self.n = 4;
        self.x = np.array([0.0, 1.0, 2.0, 2.5]);
        self.y = np.array([0.0, 0.0, 0.0, 0.0]);
        self.phi = np.array([0.0, 0.0, 0.0, 0.0]);
        self.conn = [[1, ], [0, 2], [1, 3], [2, ]];

    def pos(self, k):
        return np.array([self.x[k], self.y[k], self.phi[k]]);

    def posIs (self, k, u):
        self.x[k] = u[0];
        self.y[k] = u[1];
        self.phi[k] = u[2];
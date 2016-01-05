import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt
"""
class Nodes:
    def __init__(self, n):
        self.x = [0, 1]
        self.y = [0, 0]
        self.phi = [0, 0]
        self.conn = [[1, ], [0, ]]
    def x(k):
        return np.array([self.x[k]])
    def y(k):
        return np.array([self.y[k]])
    def phi(k):
        return np.array([self.phi[k]])
    def connection(k):
        return self.conn[k]
    def pos(k):
        return np.array([self.x[k], self.y[k], self.phi[k]])

class Elements:
    k = 1;    
"""
### Initial setting: Spring element case

def node_pos(x, y, phi, k):
    return np.array([x[k], y[k], phi[k]]);

n = 3; n_elem = 2;
kc = 1;

x0 = np.array([0, 1, 2]); y0 = np.array([0.0, 0.0, 0.0]); phi0 = np.array([0, 0, 0]);
l0 = np.array([1, 1]);
n1 = [0, 1]; n2 = [1, 2];

x = np.array([0, 1, 1.8]); y = y0; phi = phi0;
u = node_pos(x, y, phi, 1);

# Newton-Rhapson Optimization of The Potential Energy
def PotentialEnergy(u, n, n_elem, x0, y0, phi0, l0, kc, n1, n2):
    U = 0;
    x1 = np.array(x0);
    y1 = np.array(y0);
    x1[1] = x1[1] + u[0]
    y1[1] = y1[1] + u[1]
    print x1, y1
    for i in range(n_elem):
        l = np.sqrt((x1[n1[i]]-x1[n2[i]])**2 + (y1[n1[i]]-y1[n2[i]])**2);
        U = U + .5*kc*(l-l0[i])**2;
    print U
    return U;

print sp.optimize.minimize(PotentialEnergy, np.array([0.1, 0.1, 0.0]), args=(n, n_elem, x, y, phi, l0, kc, n1, n2));

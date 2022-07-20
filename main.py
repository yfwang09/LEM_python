import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt

import Nodes
import Elements

### Initial setting: Spring element case

node_ = Nodes.Nodes(20, crack=(8, 10))
elem_ = Elements.Elements(node_)

fig, ax = plt.subplots()
elem_.visualize2D(figax=(fig, ax), show=False, color=':C0')
node_.visualize2D(figax=(fig, ax), show=False, color='.k')
fig.savefig('Figure_crack_1.png')

# Set up boundary condition (Degrees of freedom)
dof_index = np.zeros_like(node_.u, dtype=bool)
interior_node_index = np.isin(np.arange(node_.n), np.arange(node_.nx, node_.n - node_.nx))
dof_index[interior_node_index, :2] = True                   # all interior nodes are DOFs (x, y coords)
dof_index[np.logical_not(interior_node_index), 0] = True    # all boundary nodes x are allowed to move
dof_index[0, 0] = False                                     # anchor point at the lower left

# Set up initial condition
ey = -0.1
node_.u[np.logical_not(interior_node_index), 1] *= (1-ey)

u0 = node_.u[dof_index].copy()
res = sp.optimize.minimize(elem_.U_pot, u0, args=(dof_index))
node_.u[dof_index] = res.x

fig, ax = plt.subplots()
elem_.visualize2D(figax=(fig, ax), show=False, color='C1')
node_.visualize2D(figax=(fig, ax), show=False, color='or')

fig.savefig('Figure_crack_2.png')
plt.show()

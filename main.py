import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt

import Nodes
import Elements

### Initial setting: Spring element case

node_ = Nodes.Nodes();
elem_ = Elements.Elements(node_);
bc_index = range(10, 90);

plt.figure()
plt.plot(node_.x, node_.y, '.k')
for i in range(elem_.n):
    plt.plot([node_.x[elem_.node[i][0]], node_.x[elem_.node[i][1]]], [node_.y[elem_.node[i][0]], node_.y[elem_.node[i][1]]], 'b')
plt.grid(True)

node_.y = np.repeat(np.array(range(10))*np.sqrt(2)/2, 10);

# Newton-Rhapson Optimization of The Potential Energy
def PotentialEnergy(u, node_, elem_, bc_index):
    U = 0;
    for i in range(len(bc_index)):
        node_.posIs(bc_index[i], u[i*3:i*3+3]);
    for i in range(elem_.n):
        #print i, elem_.node[i][0], elem_.node[i][1]
        x1 = node_.pos(elem_.node[i][0])[0];
        x2 = node_.pos(elem_.node[i][1])[0];
        y1 = node_.pos(elem_.node[i][0])[1];
        y2 = node_.pos(elem_.node[i][1])[1];
        l = np.sqrt((x1 - x2)**2 + (y1 - y2)**2);
        U = U + .5*elem_.kc[i]*(l-elem_.l0[i])**2;
    return U;

u0 = np.array([])
for i in bc_index:
    #print i, node_.pos(i)
    u0 = np.append(u0, node_.pos(i))

res = sp.optimize.minimize(PotentialEnergy, u0, args=(node_, elem_, bc_index));

# Visualization
plt.figure()
for i in range(len(bc_index)):
    node_.posIs(bc_index[i], res.x[i*3:i*3+3]);
plt.plot(node_.x, node_.y, '.k')
for i in range(elem_.n):
    plt.plot([node_.x[elem_.node[i][0]], node_.x[elem_.node[i][1]]], [node_.y[elem_.node[i][0]], node_.y[elem_.node[i][1]]], 'b')
plt.grid(True)
plt.show()


import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt

import Nodes
import Elements

### Initial setting: Spring element case

node_ = Nodes.Nodes();
elem_ = Elements.Elements(node_);
bc_index = range(node_.nc,node_.n-node_.nc);

plt.figure()
plt.plot(node_.u[:, 0], node_.u[:, 1], '.k')
for i in range(elem_.n):
    plt.plot([node_.u[elem_.node[i][0], 0], node_.u[elem_.node[i][1], 0]], [node_.u[elem_.node[i][0], 1], node_.u[elem_.node[i][1], 1]], 'b:')
plt.grid(True)

node_.u[:,1] = np.repeat(np.array(range(node_.nc))*np.sqrt(2)/2, node_.nc);

### Newton-Rhapson Optimization of The Potential Energy
def PotentialEnergy(u, node_, elem_, bc_index):
    U = 0;
    node_.u[:node_.nc, 0] = u[:node_.nc].transpose();
    for i in range(len(bc_index)):
        node_.posIs(bc_index[i], u[i*3+node_.nc:i*3+node_.nc+3]);
    node_.u[-node_.nc:, 0] = u[-node_.nc:].transpose();
    for i in range(elem_.n):
        x1 = node_.pos(elem_.node[i][0])[0];
        x2 = node_.pos(elem_.node[i][1])[0];
        y1 = node_.pos(elem_.node[i][0])[1];
        y2 = node_.pos(elem_.node[i][1])[1];
        l = np.sqrt((x1 - x2)**2 + (y1 - y2)**2);
        U = U + .5*elem_.kc[i]*(l-elem_.l0[i])**2;
    return U;

u0 = np.array([])
u0 = np.append(u0, node_.u[:node_.nc, 0].transpose())
for i in bc_index:
    u0 = np.append(u0, node_.pos(i))
u0 = np.append(u0, node_.u[-node_.nc:, 0].transpose())
#print node_.u

res = sp.optimize.minimize(PotentialEnergy, u0, args=(node_, elem_, bc_index));

### Visualization
#plt.figure()
node_.u[:node_.nc, 0] = res.x[:node_.nc].transpose();
for i in range(len(bc_index)):
    node_.posIs(bc_index[i], res.x[i*3+node_.nc:i*3+node_.nc+3]);
node_.u[-node_.nc:, 0] = res.x[-node_.nc:].transpose();
plt.plot(node_.u[:, 0], node_.u[:, 1], '.k')
for i in range(elem_.n):
    plt.plot([node_.u[elem_.node[i][0], 0], node_.u[elem_.node[i][1], 0]], [node_.u[elem_.node[i][0], 1], node_.u[elem_.node[i][1], 1]], 'r')
plt.grid(True)
#plt.ylim((0,16))

plt.show()



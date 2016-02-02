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

ey = 0.1;
node_.u[:,1] = np.repeat(np.array(range(node_.nc))*np.sqrt(3)/2*(1-ey), node_.nc);

### Newton-Rhapson Optimization of The Potential Energy
def PotentialEnergy(u, node_, elem_, bc_index):
    U = 0
    node_.u[:node_.nc, 0] = u[:node_.nc].transpose();
    for i in range(len(bc_index)):
        node_.posIs(bc_index[i], u[i*3+node_.nc:i*3+node_.nc+3]);
    node_.u[-node_.nc:, 0] = u[-node_.nc:].transpose();
    for i in range(elem_.n):
        U += elem_.Ue(i)
    return U;

u0 = np.array([])
u0 = np.append(u0, node_.u[:node_.nc, 0].transpose())
for i in bc_index:
    u0 = np.append(u0, node_.pos(i))
u0 = np.append(u0, node_.u[-node_.nc:, 0].transpose())

res = sp.optimize.minimize(PotentialEnergy, u0, args=(node_, elem_, bc_index));

### Visualization
node_.u[:node_.nc, 0] = res.x[:node_.nc].transpose();
for i in range(len(bc_index)):
    node_.posIs(bc_index[i], res.x[i*3+node_.nc:i*3+node_.nc+3]);
node_.u[-node_.nc:, 0] = res.x[-node_.nc:].transpose();

f = open("result_"+str(node_.n)+".txt", "w")
e_l = 0; e_r = 0;
for i in range(0, node_.n, node_.nc):
    e_l = e_l + node_.u[i][0]
    e_r = e_r + node_.u[i+node_.nc-1][0]
e_l = e_l/node_.nc; e_r = e_r/node_.nc;
#ey = 0.01;
nu = ((e_r-e_l)/(node_.nc-1) - 1)/ey
#print e_l, e_r
f.write("Poisson's Ratio: " + str(nu) + '\n');
f.write(str(res))
for i in range(node_.n):
    f.write(str(node_.pos(i))+'\n')
f.close()

plt.plot(node_.u[:, 0], node_.u[:, 1], '.k')
for i in range(elem_.n):
    plt.plot([node_.u[elem_.node[i][0], 0], node_.u[elem_.node[i][1], 0]], [node_.u[elem_.node[i][0], 1], node_.u[elem_.node[i][1], 1]], 'r')
plt.grid(True)

plt.show()

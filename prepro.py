import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

### 2D rectangular sample - triangulation ###

width = 80.0
height = 65.0
d = 2.0
hd = d*np.sqrt(3)/2;

nx = int(np.ceil(width / d))
ny = int(np.ceil(height / hd))

f = open('input_file.txt', 'w')
f.write('# Output file for prepro_v_0\n')
f.write('# An input file for nodes and element information.\n')

print nx, ny

# Build up node locations and properties

line_0 = np.array(range(nx)) * d
line_1 = np.array(range(nx)) * d + d / 2

print line_0, line_1

node_x = np.tile(np.hstack((line_0, line_1)), ny / 2)
node_y = np.repeat(np.array( range(ny)) * hd, nx )

print len(node_x), len(node_y)

# Assign node type

node_m = node_y<(height/2) # True = A, False = B
n_node = len(node_x)

# Output of node information

f.write('# number of nodes\n')
f.write('# node_ID material x y (z)\n')
f.write('NODE\n')
f.write(str(n_node)+'\n')
for i in range(n_node):
    xi = node_x[i]; yi = node_y[i];
    if node_m[i]:
        mi = 'A'
    else:
        mi = 'B'
    f.write(str(i)+' '+mi+' '+str(node_x[i])+' '+str(node_y[i])+'\n')

# build up element connections

elem_id = 0
elem_list = []
pre_crack = ((26.0, 54.0), (height/2, height/2))
print pre_crack

def check_pre_crack(pre_crack, xi, yi, xj, yj):
    crack_p1 = np.array([pre_crack[0][0], pre_crack[1][0]])
    crack_p2 = np.array([pre_crack[0][1], pre_crack[1][1]])
    #print 'crack_p1:', crack_p1
    #print 'crack_p2:', crack_p2
    elem_p1 = np.array([xi, yi]); elem_p2 = np.array([xj, yj]);
    d1 = np.cross(crack_p2-crack_p1, elem_p1-crack_p1)
    d2 = np.cross(crack_p2-crack_p1, elem_p2-crack_p1)
    d3 = np.cross(elem_p2-elem_p1, crack_p1-elem_p1)
    d4 = np.cross(elem_p2-elem_p1, crack_p2-elem_p1)
    return (d1*d2<0 and d3*d4<0)

for i in range(n_node):
    for j in range(i+1, n_node):
        xi = node_x[i]; yi = node_y[i]; mi = node_m[i];
        xj = node_x[j]; yj = node_y[j]; mj = node_m[j];
        dist = np.sqrt( (xi-xj)**2 + (yi-yj)**2 )
        if dist > 1.2*d:
            continue
        new_elem = [elem_id, i, j]
        elem_id += 1
        if check_pre_crack(pre_crack, xi, yi, xj, yj):
            interface = 'x'
        else:
            interface = '-'
        if mi == mj:
            if mi:
                new_elem.append('A'+interface+'A')
            else:
                new_elem.append('B'+interface+'B')
        else:
            new_elem.append('A'+interface+'B')
        elem_list.append(new_elem)

# Output of element information

f.write('\n# number of elements\n')
f.write('# elem_ID node_id_i node_id_j interface\n')
f.write('ELEMENT\n')
f.write(str(len(elem_list))+'\n')
for e in elem_list:
    f.write(str(e[0])+' '+str(e[1])+' '+str(e[2]) + ' ' + e[3] + '\n')

# Build up boundary nodes

bd_top = ~(node_y < node_y.max())
bd_bottom = ~(node_y > node_y.min())

# Output of boundary node list

f.write('\n# number of boundaries\n')
f.write('# boundary_name boundary_node_number boundary_node_list\n')
f.write('BOUNDARY\n')
f.write('2\n')
f.write('TOP\n')
f.write(str(np.count_nonzero(bd_top))+'\n')
for i in range(len(bd_top)):
    if bd_top[i]:
        f.write(str(i)+'\n')
f.write('BOTTOM\n')
f.write(str(np.count_nonzero(bd_bottom))+'\n')
for i in range(len(bd_bottom)):
    if bd_bottom[i]:
        f.write(str(i)+'\n')

f.close()

# Test of the connectivity

plt.figure()
for e in elem_list:
    ni = e[1]; nj = e[2];
    elem_x = [node_x[ni], node_x[nj]]
    elem_y = [node_y[ni], node_y[nj]]
    mi = node_m[ni]; mj = node_m[nj];
    if e[3] == 'A-A':
        color = 'r'
    elif e[3] == 'B-B':
        color = 'b'
    elif e[3] == 'A-B':
        color = 'g'
    else:
        continue
    plt.plot(elem_x, elem_y, color)
plt.plot(node_x, node_y, 'ko')
plt.plot(node_x[bd_top], node_y[bd_top], 'go')
plt.plot(node_x[bd_bottom], node_y[bd_bottom], 'go')

plt.show()



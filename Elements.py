import numpy as np

class Elements:
    def __init__(self, n_elements, nodes):
        self.n = n_elements
        self._nodes = nodes
        self._interface = [' '] * n_elements
        self._conn = [()] * n_elements
        
        #self.node_ = nodes;
        #self.n = (node_.nc-1)*(3*node_.nc-1);
        self.l0 = np.repeat([10.0], self.n);
        self.E = 1.0;
        self.nu = 0.6;
        self.D = np.diag([self.E, self.E*self.nu, self.E]);
        self.theta0 = np.repeat([0.0], self.n);
        """
        nc = nodes.nc;
        next_node = [1, nc-1, nc, nc+1];
        for i in range(node_.n):
            for next in next_node:
                if i + next >= node_.n:
                    continue;
                if np.linalg.norm(node_.pos(i)-node_.pos(i+next)) < 1.1:
                    self.node.append((i, i+next));
                    node_i = node_.u0[i][:];
                    node_j = node_.u0[i+next][:];
                    self.theta0.append(np.arctan2(node_j[1]-node_i[1], node_j[0]-node_i[0]))
        """

    def elementIs (self, nid, node_i, node_j, interface):
        self._conn[nid] = (node_i, node_j)
        self._interface[nid] = interface
        x_i = self._nodes.pos(node_i)
        x_j = self._nodes.pos(node_j)
        self.theta0[nid] = np.arctan2(x_j[1]-x_i[1], x_j[0]-x_i[0])

    def du (self, n):
        dnode_i = self._nodes.displacement(self._conn[n][0]);
        dnode_j = self._nodes.displacement(self._conn[n][1]);
        return np.concatenate((dnode_i, dnode_j));

    def K (self, n):
        alpha = self.theta0[n];#np.arctan2(node_j[1]-node_i[1], node_j[0]-node_i[0])-self.theta0[n];
        c = np.cos(alpha); s = np.sin(alpha);
        e = 0; h = self.l0[n]; t = 1.0; l = h/np.sqrt(3);
        A = l*t; I = 0.2*(l**3)*t/12; E = 1.0;
        EA = E*A; EI = E*I;
        T = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]]);
        Z = np.zeros((3,3))
        B = np.vstack((np.hstack((T,Z)),np.hstack((Z,T))))
        D = np.array([[-EA/l,   0,  0,  EA/l,   0,  0],\
                      [0, -12*EI/(l**3), -6*EI/(l**2), 0, 12*EI/(l**3), -6*EI/(l**2)],\
                      [0, -6*EI/(l**2),  -4*EI/l,      0, 6*EI/(l**2),  -2*EI/l],\
                      [EA/l,   0,  0,  -EA/l,   0,  0],\
                      [0, 12*EI/(l**3),   6*EI/(l**2), 0, -12*EI/(l**3),6*EI/(l**2)],\
                      [0, -6*EI/(l**2),  -2*EI/l,      0, 6*EI/(l**2), -4*EI/l]])
        #duc = np.dot(B, np.concatenate((dnode_i, dnode_j)))
        #q = A/h*np.dot(self.D, duc)
        #return A/h*np.dot(np.dot(B.transpose(), self.D), B);
        return np.dot(np.dot(B.transpose(), D), B)

    def f (self, n):
        #node_i = self.node_.pos(self.node[n][0]);
        #node_j = self.node_.pos(self.node[n][1]);
        return np.dot(self.K(n), self.du(n));
        #print dnode_i, dnode_j, alpha*180/np.pi, c, s
        #print B
        #print duc, q
        #print self.D
        #print K

    def Ue (self, n):
        return np.dot(self.f(n), self.du(n));
    

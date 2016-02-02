import numpy as np

class Elements:
    def __init__(self, node_):
        self.node_ = node_;
        self.n = (node_.nc-1)*(3*node_.nc-1);
        self.l0 = np.repeat([1.0], self.n);
        self.E = 1.0;
        self.nu = 0.6;
        self.D = np.diag([self.E, self.E*self.nu, self.E]);
        self.node = [];
        self.theta0 = [];
        nc = node_.nc;
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

    def du (self, n):
        dnode_i = self.node_.displacement(self.node[n][0]);
        dnode_j = self.node_.displacement(self.node[n][1]);
        return np.concatenate((dnode_i, dnode_j));

    def K (self, n):
        alpha = self.theta0[n];#np.arctan2(node_j[1]-node_i[1], node_j[0]-node_i[0])-self.theta0[n];
        c = np.cos(alpha); s = np.sin(alpha);
        e = 0; h = self.l0[n]; t = 1.0; l = h/np.sqrt(3);
        A = l*t; I = l**3*t/12;
        B = np.array([[-c, -s, -e, c, s, e], [s, -c, -h/2, -s, c, -h/2],\
                      [0, 0, np.sqrt(I/A), 0, 0, np.sqrt(I/A)]]);
        #duc = np.dot(B, np.concatenate((dnode_i, dnode_j)))
        #q = A/h*np.dot(self.D, duc)
        return A/h*np.dot(np.dot(B.transpose(), self.D), B);
    
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
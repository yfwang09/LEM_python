import numpy as np

class Elements:
    def __init__(self, node_):
        self.node_ = node_;
        self.n = (node_.nc-1)*(3*node_.nc-1);
        self.l0 = np.repeat([1.0], self.n);
        self.E = 1.0;
        self.nu = 0.2;
        self.D = np.diag([self.E, self.E*self.nu, self.E]);
        self.node = [];
        nc = node_.nc;
        next_node = [1, nc-1, nc, nc+1];
        for i in range(node_.n):
            for next in next_node:
                if i + next >= node_.n:
                    continue;
                if np.linalg.norm(node_.pos(i)-node_.pos(i+next)) < 1.1:
                    self.node.append((i, i+next));
                    node_i = node_.pos(i);
                    node_j = node_.pos(i+next);

    def forceResponce (self, n):
        node_i = self.node_.pos(self.node[n][0]);
        node_j = self.node_.pos(self.node[n][1]);
        dnode_i = self.node_.displacement(self.node[n][0]);
        dnode_j = self.node_.displacement(self.node[n][1]);
        alpha = np.arctan2(node_j[1] - node_i[1], node_j[0] - node_i[0]);
        c = np.cos(alpha); s = np.sin(alpha);
        e = 0; h = self.l0[n]; t = 1.0; l = h/np.sqrt(3);
        A = l*t; I = l**3*t/12;
        B = np.array([[-c, -s, -e, c, s, e], [s, -c, -h/2, c, s, -h/2],\
                      [0, 0, np.sqrt(I/A), 0, 0, np.sqrt(I/A)]]);
        K = A/h*np.dot(np.dot(B.transpose(), self.D), B);
        f = np.dot(K, np.concatenate((dnode_i, dnode_j)));
        print node_i, node_j, dnode_i, dnode_j, alpha*180/np.pi, c, s
        print B
        print self.D
        print K
        return f

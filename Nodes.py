import numpy as np

class Nodes:
    def __init__(self):
        nc = 10;
        self.n = 100;
        self.x = np.tile(np.hstack((np.array(range(10)),(np.array(range(10)) - 0.5))), 5);
        self.y = np.repeat(np.array(range(10))*np.sqrt(3)/2, 10);
        self.phi = np.zeros(100);
        self.conn = [];
        next_node = [-1, 1, -nc-1, -nc, -nc+1, nc-1, nc, nc+1];
        for i in range(self.n):
            conn_ = [];
            for next in next_node:
                if i+next >= self.n:
                    continue;
                if np.linalg.norm(self.pos(i)-self.pos(i+next)) < 1.1:
                    conn_.append(i+next);
            self.conn.append(conn_);

    def pos(self, k):
        return np.array([self.x[k], self.y[k], self.phi[k]]);

    def posIs (self, k, u):
        self.x[k] = u[0];
        self.y[k] = u[1];
        self.phi[k] = u[2];
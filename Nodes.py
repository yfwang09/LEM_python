import numpy as np

class Nodes:
    def __init__(self):
        self.nc = 6;
        self.n = self.nc**2;
        nc = self.nc;
        x = np.tile(np.hstack((np.array(range(nc)),(np.array(range(nc)) - 0.5))), nc//2);
        y = np.repeat(np.array(range(nc))*np.sqrt(3)/2, nc);
        phi = np.zeros(self.n);
        self.u0 = np.vstack((x, y, phi)).transpose();
        self.u = np.vstack((x, y, phi)).transpose();
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

    def pos (self, k):
        return self.u[k][:];

    def posIs (self, k, u):
        self.u[k][:] = u;

    def displacement (self, k):
        return self.u[k][:] - self.u0[k][:];
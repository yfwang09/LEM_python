import numpy as np

class Elements:
    def __init__(self, node_):
        self.n = (node_.nc-1)*(3*node_.nc-1);
        self.l0 = np.repeat([1.0], self.n);
        self.kc = np.repeat([1.0], self.n);
        self.node = [];
        nc = node_.nc;
        next_node = [1, nc-1, nc, nc+1];
        for i in range(node_.n):
            for next in next_node:
                if i+next >= node_.n:
                    continue;
                if np.linalg.norm(node_.pos(i)-node_.pos(i+next)) < 1.1:
                    self.node.append((i, i+next));

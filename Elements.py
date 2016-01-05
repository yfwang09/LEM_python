import numpy as np

class Elements:
    def __init__(self):
        self.n = 3;
        self.l0 = np.array([1.0, 1.0, 1.0]);
        self.kc = np.array([1.0, 1.0, 1.0]);
        self.node = ((0, 1), (1, 2), (2, 3));

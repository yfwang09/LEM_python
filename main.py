import numpy as np
import scipy as sp
import scipy.optimize
import matplotlib.pyplot as plt

### Initial setting: Beam bending case

n = 3; nv = 2;
EA = 62; EI = 10;
L = 1;   nu = 0;
GA = 0.5*EA/(1+nu);
kc = (10+10*nu)/(12+11*nu);
ke = np.array([[EA/L,   0,          0,          -EA/L,  0,          0           ],\
               [0,      12*EI/L**3, 6*EI/L**2,  0,      -12*EI/L**3,6*EI/L**2   ],\
               [0,      6*EI/L**2,  4*EI/L,     0,      -6*EI/L**2, 2*EI/L      ],\
               [-EA/L,  0,          0,          EA/L,   0,          0           ],\
               [0,      -12*EI/L**3,-6*EI/L**2, 0,      12*EI/L**3, -6*EI/L**2  ],\
               [0,      6*EI/L**2,  2*EI/L,     0,      -6*EI/L**2, 4*EI/L      ]]);

ue0 = np.array([0, 0, 0, 1, 0, 0, 2, 0, 0]);
pert = np.array([0, 0, 0, 0, 0, 0, 0, 0.01, 0]);

ue = ue0 + pert;
print ue

# Newton-Rhapson Optimization of The Potential Energy
def PotentialEnergy(u, ue0, nv, ke, L, EA, EI, kc, GA):
    U = 0;
    ue = ue0; ue[3:-3] = ue[3:-3] + u;
    print ue
    for i in range(nv):
        fe = np.dot(ke, np.transpose(ue[(i*3):(i*3+6)]));
        UF = 0.5*(fe[0]**2)*L/EA;
        UQ = 0.5*(fe[1]*fe[1])*L/kc/GA;
        UM = 0.5*(fe[2]*fe[2])*L/EI;
        U = U + UF+UQ+UM;
        print i, fe, UF, UQ, UM, U
    return U;

print sp.optimize.minimize(PotentialEnergy, np.zeros(3), args=(ue, nv, ke, L, EA, EI, kc, GA));

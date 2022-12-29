import numpy as np
import scipy.stats as st
from scipy.integrate import quad

print(quad(st.norm.pdf, -10, 10))


def RR(F):
    FF = st.norm.pdf / (1 - st.norm.cdf)
    GG = st.norm.pdf / (1 - st.norm.cdf)

    def evaluate(x):
        I1 = quad(FF, -np.inf, x)
        I2 = quad(GG, -np.inf, x)
        return I1 / (I1 + I2)

    return evaluate

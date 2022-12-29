import numpy as np
import scipy.stats as st
from scipy.integrate import quad
from scipy.optimize import root

f = lambda y: quad(lambda x: (1 - st.gamma.cdf(x, a=1, loc=y)) * st.expon.pdf(x), -np.inf, np.inf)[
                        0] - 0.3
print(root(f, 1).x)
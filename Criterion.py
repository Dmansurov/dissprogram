import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt
from statsmodels.distributions import ECDF


class Criterion:

    def __init__(self, senzur, n):
        self.distribution = ''
        self.scale = 1
        self.dist = st.norm
        TT = np.array([])
        for i in range(5000):
            T, pn = self.RandomSample(senzur, n)
            H = ECDF(T)
            H1 = ECDF(T, side="left")
            Baho = lambda xx: 1 - np.power(1 - H(xx), pn)
            Baho1 = lambda xx: 1 - np.power(1 - H1(xx), pn)
            a = np.max(np.abs(self.dist.cdf(T, scale=self.scale) - Baho(T)))
            b = np.max(np.abs(self.dist.cdf(T, scale=self.scale) - Baho1(T)))
            TT = np.append(np.fmax(a, b), TT)
        N = np.histogram((np.sqrt(n / np.log(np.log(n)))) * TT, bins='auto')
        self.distribution = st.rv_histogram(N)

    def RandomSample(self, senzur, n):

        tetta = senzur / (n - senzur)
        Ftanlanma = self.dist.isf(1 - st.uniform.rvs(size=n), scale=self.scale)
        if tetta != 0:
            Gtanlanma = self.dist.isf(np.power((1 - st.uniform.rvs(size=n)), 1 / tetta), scale=self.scale)
        else:
            Gtanlanma = np.full(n, np.inf)
        E = np.zeros(n)
        E[Ftanlanma <= Gtanlanma] = 1
        if n - np.sum(E) == senzur:
            self.T = np.fmin(Ftanlanma, Gtanlanma)
        else:
            self.RandomSample(senzur, n)
        return self.T, np.mean(E)



t = Criterion(10, 100)
#x = np.linspace(-1, 2)
#y = t.distribution.cdf(x)
#plt.plot(x, y)
#plt.show()
print(t.distribution.cdf(1))

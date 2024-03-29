import numpy as np
from scipy.stats import expon, rv_histogram, uniform
from statsmodels.distributions import ECDF


def Statistika_qiymati(xt, xp, taqsimot=expon):
    n = len(xt)
    H = ECDF(xt)
    H1 = ECDF(xt, side="left")
    Baho = lambda xx: 1 - np.power(1 - H(xx), xp)
    Baho1 = lambda xx: 1 - np.power(1 - H1(xx), xp)
    a = np.max(np.abs(taqsimot.cdf(xt) - Baho(xt)))
    b = np.max(np.abs(taqsimot.cdf(xt) - Baho1(xt)))
    return np.fmax(a, b) * (np.sqrt(n / np.log(np.log(n))))


class Criterion:

    def __init__(self, senzur, n):
        self.T = []
        self.distribution = ''
        TT = np.array([])
        for c in range(15000):
            T, pn = self.RandomSample(senzur, n)
            TT = np.append(TT, Statistika_qiymati(T, pn))
        N = np.histogram(TT, bins='auto')
        self.distribution = rv_histogram(N)

    def RandomSample(self, senzur, n):
        tetta = senzur / (n - senzur)
        Ftanlanma = expon.isf(1 - uniform.rvs(size=n))
        if tetta != 0:
            Gtanlanma = expon.isf(np.power((1 - uniform.rvs(size=n)), 1 / tetta))
        else:
            Gtanlanma = np.full(n, np.inf)
        E = np.zeros(n)
        E[Ftanlanma <= Gtanlanma] = 1
        if n - np.sum(E) == senzur:
            self.T = np.fmin(Ftanlanma, Gtanlanma)
        else:
            self.RandomSample(senzur, n)
        return self.T, np.mean(E)


if __name__ == '__main__':
    t = Criterion(1000, 5000)
    print(t.distribution.cdf(0.9))

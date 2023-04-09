import pandas as pd
import numpy as np
import scipy.stats

class BetaDist(object):

    def __init__(self, bola):
        self._bola = bola
        df = pd.read_csv("lotomania_result.csv")
        arrBola = df[self.get_bola()]
        self._mean = np.mean(arrBola)
        self._std = np.std(arrBola)
        self._min = np.min(arrBola)
        self._max = np.max(arrBola)

    def get_bola(self):
        return self._bola
    
    def get_mean(self):
        return self._mean
    
    def get_std(self):
        return self._std
    
    def get_min(self):
        return self._min
    
    def get_max(self):
        return self._max

    def pdf(self):
        min_val = self.get_min()
        max_val = self.get_max()
        mean = self.get_mean()
        std = self.get_std()
        
        scale = max_val - min_val
        location = min_val
        # Mean and standard deviation of the unscaled beta distribution
        unscaled_mean = (mean - min_val) / scale
        unscaled_var = (std / scale) ** 2
        # Computation of alpha and beta can be derived from mean and variance formulas
        t = unscaled_mean / (1 - unscaled_mean)
        beta = ((t / unscaled_var) - (t * t) - (2 * t) - 1) / ((t * t * t) + (3 * t * t) + (3 * t) + 1)
        alpha = beta * t
        # Not all parameters may produce a valid distribution
        if alpha <= 0 or beta <= 0:
            raise ValueError('Cannot create distribution for the given parameters.')
        # Make scaled beta distribution with computed parameters
        return scipy.stats.beta(alpha, beta, scale=scale, loc=location)

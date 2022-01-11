import numpy as np
import matplotlib.pylab as plt
import ruptures as rpt
# creation of data
n, dim = 500, 1  # number of samples, dimension
n_bkps, sigma = 3, 5  # number of change points, noise standart deviation
signal, bkps = rpt.pw_constant(n, dim, n_bkps, noise_std=sigma)
print(signal)
c = rpt.costs.CostL1().fit(signal)
print(c.sum_of_costs([10, 100, 200, 250, n]))
import numpy as np
from scipy.stats import multinomial

p = [0.082, 0.015, 0.028, 0.043, 0.13, 0.021, 0.02, 0.06, 0.07, 0.0014, 0.0077, 0.04, 0.023, 0.067, 0.075, 0.019, 0.00095, 0.06, 0.063, 0.09, 0.028, 0.0098, 0.024, 0.0014, 0.02, 0.00075] # frequency of each letter

def log_factorial(n):
	ans = sum([np.log(i) for i in range(1,n+1)])
	return ans

def compute_probs(N):
	rv = multinomial(N,p)
	samples = rv.rvs(size=20)

	probs = []
	for x in samples:
		# compute logarithm of probability first
		lp = log_factorial(N)
		lp -= sum([log_factorial(k) for k in x])
		lp += sum([x[i] * np.log(p[i]) for i in range(26)])
		prob = np.exp(lp)
		probs.append(prob)

	return probs
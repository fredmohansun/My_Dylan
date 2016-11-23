# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:28:03 2016

@author: sunmohan
Monte Carlo experiment
"""

import numpy as np
import scipy as sp

K = 40
T = 1
S0 = 41
sigma = .3
r = .08
div = 0
N = 3
M = 10000

h = T/N
nuh = (r-div-0.5*sigma*sigma)*h
sigsh = np.sqrt(h) * sigma
X0 = np.log(S0)
np.random.seed(1234)

sum_payoff = 0.0
sum_payoff2 = 0.0

for i in range(M):
    X1 = X0
    X2 = X0
    for j in range(N):
        eps = float(np.random.standard_normal(1))
        X1 += nuh + sigsh * eps
        X2 += nuh - sigsh * eps
    
    S1 = np.exp(X1)
    S2 = np.exp(X2)
    payoff = 0.5*max(S1-K,0)+0.5*max(S2-K,0)
    sum_payoff += payoff
    sum_payoff2 += payoff*payoff
    
call_value = sum_payoff/M * np.exp(-r*T)

print(call_value)
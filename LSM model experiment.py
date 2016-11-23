# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:14:17 2016

@author: sunmohan
LSM model experiment
"""

import numpy as np

## Setting Parameters

K = 40
T = 1
S0 = 41
sigma = .3
r = .08
div = 0
N = 3
M = 10000

## Calculating Parameters
h = T/N
nuh = (r-div-0.5*sigma*sigma)*h
sigsh = np.sqrt(h) * sigma

## X is for log(S)
X0 = np.log(S0)
X = np.zeros((M,N+1))

## Calculate X for N steps for M simulation, and get S matrix by exp(X)
for j in range(M):
    X[j][0]=X0
    for i in range(1,N+1):
        eps = float(np.random.standard_normal(1))
        X[j][i] = X[j][i-1] +nuh +sigsh *eps
    
S = np.exp(X)

## CF is the matrix of value of option at each step, column 0 is an index
## Last column, or value at expiry, is the payoff at expury
CF = np.zeros((M,N+2))
CF[:,N+1] = np.maximum(K-S[:,N],0)

for i in range(M):
    CF[i][0]=i

## Recursion part on calculating CF
for i in range(N-1,0,-1):
    
## Stemp is the column drawn from S, indStemp is used to check if option is in the money
    Stemp = S[:,i]
    indStemp = Stemp < K
    
## Numtemp contains the row index of each dataset
    Numtemp = CF[:,0]
    
## CFtemp is the PV of continuation value at the time horizon t = i
    ncol = (N+1)-(i+2)+1
    CFtemp1 = np.zeros((M,ncol))
    for k in range(ncol):
        CFtemp1[:,k] = CF[:,i+2+k]
        
    CFtemp = np.zeros(M)
        
    for j in range(M):
        for k in range(ncol):
            CFtemp[j] += CFtemp1[j][k] * np.exp(-r*h*(k+1))
    

    size = len(Stemp[indStemp])

## include only the simulation where the option is in the money at t = i    
    regression = np.zeros((size,3))
    regression[:,0] = Stemp[indStemp]
    regression[:,1] = Stemp[indStemp] ** 2
    regression[:,2] = CFtemp[indStemp]
    
## Linear Regression
    X = np.ones((len(Stemp[indStemp]),3))
    X[:,[0,1]] = regression[:,[0,1]]
    Y = regression[:,2]
    
    beta1, beta2, beta0 = np.linalg.lstsq(X,Y)[0]

## Calculate predict PV of Contiunation value and get the payoff at t = i
    CVhat = beta0 + beta1 * X[:,0] + beta2 * X[:,1]    
    Payofftemp = np.maximum(K-X[:,0],0)    
    Num = Numtemp[indStemp]
    
## if the PV of continuation value is less than payoff at t = i, individual
## choose to exercise early and get the payoff
    for j in range(size):
        if CVhat[j] < Payofftemp[j]:
                CF[Num[j]][i+1] = Payofftemp[j]
                CF[Num[j]][i+2] = 0.0
                
## End of recursion

Sum = 0.0    

## the value of option for each simulation is the sum of all PV of continuation value
for j in range(M):
    for i in range(2,N+2):
        CF[j][1] += CF[j][i] * np.exp(-r*h*(i-1))
    Sum += CF[j][1]

## price is the average of all simulation
price = Sum/M

print(CF)
print(price)

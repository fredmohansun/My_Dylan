# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:52:36 2016

@author: sunmohan
"""

import abc
import numpy as np
from scipy.stats import binom

class PriceEngine(object, metaclass = abc.ABCMeta):

    @abc.abstractmethod
    def pricing(self):
        pass
    
class BinomialEngine(PriceEngine):
    
    def __init__(self, depth, pricer):
        self.__depth = depth
        self.__pricer = pricer
        
    @property
    def depth(self):
        return self.__depth
        
    @depth.setter
    def depth(self, NewDepth):
        self.__depth = NewDepth
        
    def pricing(self, option, asset):
        return self.__pricer(self, option, asset)
        
def BinomAmerican(PriceEngine, option, asset):
    (s0, r, sigma, div) = asset.GetData()
    N = PriceEngine.depth
    T = option.expiry
    h = T/N
    
    S = np.zeros((N+1,N+1))
    payoff = np.zeros((N+1,N+1))
    price = np.zeros((N+1,N+1))    
    
    u = np.exp(r*h+sigma*np.sqrt(h))
    d = np.exp(r*h-sigma*np.sqrt(h))
    pu = (np.exp(r*h)-d)/(u-d)
    pd = 1-pu

    S[0][0] = s0
    
    for i in range(1,N+1):
        for j in range(i):
            S[i][j]=S[i-1][j]*u
            payoff[i][j] = option.payoff(S[i][j])
        S[i][j+1]=S[i-1][j]*d
        payoff[i][j+1] = option.payoff(S[i][j+1])

    price[N] = payoff[N]   

    for i in range(N-1,-1,-1):
        for j in range(i+1):
            temp = (pu*price[i+1][j]+pd*price[i+1][j+1])*np.exp(-r*h)
            price[i][j] = max(payoff[i][j],temp)
    
    return price[0][0]
    
def BinomEuropean(PriceEngine, option, asset):
    (s0, r, sigma, div) = asset.GetData()
    N = PriceEngine.depth
    T = option.expiry
    h = T/N
     
    price = 0.0
    
    u = np.exp(r*h+sigma*np.sqrt(h))
    d = np.exp(r*h-sigma*np.sqrt(h))
    pu = (np.exp(r*h)-d)/(u-d)
    
    for i in range(N+1):
        S = s0 *(u**(N-i))*(d**(i))
        payoff = option.payoff(S)
        price += payoff * binom.pmf(N-i,N,pu)

    price *= np.exp(-r*T)
    return price
    
class AnalyticalEngine(PriceEngine):
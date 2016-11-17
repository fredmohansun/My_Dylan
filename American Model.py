# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:32:19 2016

@author: sunmohan
"""

import numpy as np

def OptionPrice(Option,u,d,pu,pd,t,N,h,r,sigma):
    Option.numtype()
    S = np.zeros((N+1,N+1))
    payoff = np.zeros((N+1,N+1))
    price = np.zeros((N+1,N+1))
    S[0][0] = Option.S
    for i in range(1,N+1):
        for j in range(i):
            S[i][j]=S[i-1][j]*u
            if Option.type == 1:
                payoff[i][j] = max(S[i][j]-Option.K,0)
            elif Option.type == 2:
                payoff[i][j] = max(Option.K-S[i][j],0)
        S[i][j+1]=S[i-1][j]*d
        if Option.type == 1:
                payoff[i][j+1] = max(S[i][j+1]-Option.K,0)
        elif Option.type == 2:
                payoff[i][j+1] = max(Option.K-S[i][j+1],0)
    

    price[N] = payoff[N]   
    
    print(S)
    print(payoff)
    print(price)
    
    for i in range(N-1,-1,-1):
        for j in range(i+1):
            temp = (pu*price[i+1][j]+pd*price[i+1][j+1])*np.exp(-r*h)
            price[i][j] = max(payoff[i][j],temp)

    
    print(price)
    return price[0][0]

    

class option(object):
    
    def __init__(self,S,K,type):
        self.S = S
        self.K = K
        self.t = type
        self.payout = 0
        self.type = 0
        
    def numtype(self):
        try:
            a = {'c':1, 'C':1, 'p':2, 'P':2}
            self.type = a[self.t]
        except:
            print("invalid type")
    
    def get_payout(self):
        if self.type != 1 or self.type != 2:
            self.numtype()
        if self.type == 1:
            self.payout = max(self.S-self.K,0)
        elif self.type == 2:
            self.payout = max(self.K-self.S,0)
        
        


def main():
    # S0,K,sigma,h=T/N,r,
    S0 = 41
    K=40
    N=100000
    T=1
    h=T/N
    sigma=.30
    r=.08
    u = np.exp(r*h+sigma*np.sqrt(h))
    d = np.exp(r*h-sigma*np.sqrt(h))
    pu = (np.exp(r*h)-d)/(u-d)
    pd = 1-pu
    Firstoption = option(S0,K,'p')
    price = OptionPrice(Firstoption,u,d,pu,pd,0,N,h,r,sigma)
    print(price)
    
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:32:17 2016

@author: sunmohan
"""

class asset(object):
    
    def __init__(self, S0, r, sigma, div):
        self.__spot = S0
        self.__rate = r
        self.__volatility = sigma
        self.__dividend = div
        
    @property
    def spot(self):
        return self.__spot
        
    @spot.setter
    def spot(self, NewSpot):
        self.__spot = NewSpot
            
    @property
    def rate(self):
        return self.__rate
        
    @rate.setter
    def rate(self, NewRate):
        self.__rate = NewRate
            
    @property
    def volatility(self):
        return self.__volatility
        
    @volatility.setter
    def volatility(self, NewVolatility):
        self.__volatility = NewVolatility
            
    @property
    def dividend(self):
        return self.__dividend
        
    @dividend.setter
    def dividend(self, NewDividend):
        self.__dividend = NewDividend
    
    def GetData(self):
        return (self.__spot,self.__rate,self.__volatility,self.__dividend)
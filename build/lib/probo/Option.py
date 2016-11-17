# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:34:15 2016

@author: sunmohan
"""
from numpy import maximum
import abc

class Option(object, metaclass=abc.ABCMeta):    
    @property
    @abc.abstractmethod
    def expiry(self):
        """return the expiry"""
        pass
    
    @expiry.setter
    @abc.abstractmethod
    def expiry(self, New):
        """expiry setter"""
        pass
    
    @abc.abstractmethod
    def payoff(self):
        pass
    
class VanillaOption(Option):
    
    def __init__(self, strike, expiry, payoff):
        self.__strike = strike
        self.__expiry = expiry
        self.__payoff = payoff
    
    @property
    def expiry(self):
        return self.__expiry
    
    @expiry.setter
    def expiry(self, newExpiry):
        self.__expiry = newExpiry
        
    @property
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, newStrike):
        self.__strike = newStrike
        
    def payoff(self, spot):
        return self.__payoff(self, spot)

class ExoticOption(Option):
    
    def __init__(self, strike, expiry, payoff):
        self.__strike = strike
        self.__expiry = expiry
        self.__payoff = payoff
    
    @property
    def expiry(self):
        return self.__expiry
    
    @expiry.setter
    def expiry(self, newExpiry):
        self.__expiry = newExpiry
        
    def strike(self):
        return self.__strike(self)
        
    def payoff(self, spot):
        return self.__payoff(self, spot)
        
def call(option, spot):
    return maximum(spot-option.strike,0)
    
def put(option, spot):
    return maximum(option.strike-spot,0)
    
def AsianStrike(option):
    pass
#!/usr/bin/env python
# coding: utf-8

# In[11]:


import random
import sys
from math import exp
sys.path.insert(0, 'D:\My Documents\GitHub\Elementary-Finance')
from FinancialStats import ICNF
from PayoffFunctions import EuropeanCallPayoff as ECP
from PayoffFunctions import EuropeanPutPayoff as EPP
from PayoffFunctions import DigitalCallPayoff as DCP
from PayoffFunctions import DigitalPutPayoff as DPP

def RandomVector(l,**kwargs):
    #creates a vector of length l with each element being a random draw from a distribution. 
    #It has two keyword args, Seed to set the seed otherwise set at 0, and Dist, we shall assume
    #a normal distribution is required unless specified, currfently only normal and unf are available.
    
    random.seed(0)
    I=[0]*l
    if "Seed" in kwargs:
        random.seed(kwargs["Seed"])
    for i in range(l):
        if "Dist" in kwargs:
            if kwargs["Dist"]=="Unif":
                I[i]=random.random()
            else:
                return print("Distribution is not valid.")
        else:
            I[i]=ICNF(random.random())
    return I


# In[12]:


def StockEvolver(Share,WS,T,l,**kwargs):
    #Takes a Share vector, a worldstate, a length of time T and number of samples l and produces a list of 
    #l possible share values in the future at time T B.21 of Joshi.
    r=WS[0]
    d=Share[1]
    S=Share[0]
    Vol=Share[3]
    R=RandomVector(l,**kwargs)
    I=[0]*l
    for i in range(l):
        I[i]=S*exp((r-d)*T-0.5*Vol**2*T+Vol*T**0.5*R[i])
    return I


# In[13]:


def MonteCarloPricer(O,WS,l,**kwargs):
    #Takes our evolved stock list (of one time step), computes the payoff function on it, then averages the result.
    SList=StockEvolver(O[1],WS,O[2],l,**kwargs)
    Type=O[0]
    I=["Not defined"]*l
    for i in range(l):
        I[i]=Type[1](SList[i],O[3])
    return sum(I)/l


# In[14]:





# In[ ]:





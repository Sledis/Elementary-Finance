#!/usr/bin/env python
# coding: utf-8

# In[314]:


#This will contain several derivative pricing functions for the most elementary of options, ie European
#and digital options.
#Our shares will be expressed in a 4d vector Share=[Current Price,Derivative,Drift,Vol]. It's worth noting
#here that we will not need drift, but in later programs for more complicated options drift will play a role.
#Our options will be of the form O=[Type,Share,Time,Strike].
#Our functions will then be functions on two variables, O and WS, WS being the world state, ie the cc interest rate.
from math import exp
from math import pi
from math import log
import sys
sys.path.insert(0, 'D:\My Documents\GitHub\Elementary-Finance')
from FinancialStats import NCF

#We start with the forward price of a share as given by page 25 of Joshi.
def BSF(O,WS):
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    K=O[3]
    return exp(-r*T)*(exp((r-d)*T)*S-K)


# In[315]:


#We first define the Black Scholes European call function as given by the formula
def BSC(O,WS):
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    #formula of the black sholes price of a European call option given by the formula
    if S/K>0 and Vol*T**0.5!=0:
        d_1=(log(S/K)+(r-d+0.5*Vol**2)*(T))/(Vol*T**0.5)
        d_2=(log(S/K)+(r-d-0.5*Vol**2)*(T))/(Vol*T**0.5)
        C=S*exp(-d*T)*NCF(d_1)-K*exp(-r*T)*NCF(d_2)
    else:
        return print("Undefined")
    return C


# In[316]:


#Now, the Black Scholes European put.
def BSP(O,WS):
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    if K/S>0 and Vol*T**0.5!=0:
        d_1=(log(K/S)+(-r+d+0.5*Vol**2)*(T))/(Vol*T**0.5)
        d_2=d_1-Vol*T**0.5
        C=-S*exp(-d*T)*NCF(d_2)+K*exp(-r*T)*NCF(d_1)
    else:
        return print("Undefined")
    return C


# In[317]:


#We now check that these functions are working properly by using the put-call parity theorem.
def BSCheck(O,WS):
    if type(BSC(O,WS)) is float and type(BSP(O,WS)) is float and type(BSF(O,WS)) is float:
        return BSC(O,WS)-BSP(O,WS)-BSF(O,WS)
    else:
        return print("Undefined")


# In[318]:


#We now define the Digital Call option
def DC(O,WS):
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    if K/S>0 and Vol*T**0.5!=0:
        d=(log(K/S)-(r-d-0.5*Vol**2)*T)/(Vol*T**0.5)
    else:
        return print("Undefined")
    return exp(-r*T)*NCF(-d)
    
    


# In[319]:


#We now define the Digital Put option
def DP(O,WS):
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    if K/S>0 and Vol*T**0.5!=0:
        d=(log(K/S)-(r-d-0.5*Vol**2)*T)/(Vol*T**0.5)
    
    else:
        return print("Undefined")
    return exp(-r*T)*NCF(d)


# In[320]:


#We now define the zero coupon bond, so that we can check the digitals using put call parity
def ZCB(O,WS):
    r=WS[0]
    T=O[2]
    return exp(-r*T)
#The check function for digital options based on put call parity.

def DCheck(O,WS):
    if type(DP(O,WS)) is float and type(DC(O,WS)) is float and type(ZCB(O,WS)) is float:
        return DP(O,WS)+DC(O,WS)-ZCB(O,WS)
    else:
        return print("Undefined")


# In[321]:


#We now define a big calling function. Type will also be a vector of the form Type=[Name,pay off function,*args]

def BlackScholes(O,WS):
    if O[0][0]=='EC':
        return BSC(O,WS)
    elif O[0][0]=='EP':
        return BSP(O,WS)
    elif O[0][0]=='F':
        return BSF(O,WS)
    elif O[0][0]=='DC':
        return DC(O,WS)
    elif O[0][0]=='DP':
        return DP(O,WS)
    elif O[0][0]=='ZCB':
        return ZCB(O,WS)
    else:
        return print("Not currently defined for that option.")
    


# In[322]:


#We now define a function that can take a black scholes option, world state, a greek and a step length
#then output the option and world state that would satisfy that greek and step length.
def Greek(O,WS,G,step):
    NewOption=[0]*4
    
    if G=="Delta":
        NewOption[0]=O[0]
        NewOption[1]=[O[1][0]+step,O[1][1],O[1][2],O[1][3]]
        NewOption[2]=O[2]
        NewOption[3]=O[3]
        
        return [NewOption,WS]
    
    elif G=="Vega":
        NewOption[0]=O[0]
        NewOption[1]=[O[1][0],O[1][1],O[1][2],O[1][3]+step]
        NewOption[2]=O[2]
        NewOption[3]=O[3]
        
        return [NewOption,WS]
    
    elif G=="Rho":
        return [O,[WS[0]+step]]
    
    elif G=="Theta":
        NewOption[0]=O[0]
        NewOption[1]=O[1]
        NewOption[2]=O[2]+step
        NewOption[3]=O[3]
        return [NewOption,WS]
        


# In[323]:


def BlackScholesGreeks(O,WS,G,step):
    #We now combine our greek program and our formula program to produce the greeks by approximation.
    if G in ["Delta","Vega","Rho"]:
        return (BlackScholes(*Greek(O,WS,G,step))-BlackScholes(O,WS))/step
    elif G=="Theta":
        return -(BlackScholes(*Greek(O,WS,G,step))-BlackScholes(O,WS))/step
    elif G=="Gamma":
        return (BlackScholes(*Greek(O,WS,"Delta",step))-2*BlackScholes(O,WS)+BlackScholes(*Greek(O,WS,"Delta",-step)))/step**2
        
        
    else:
        return print("Not defined for that Greek.")
    


# In[324]:



def BSDelta(O,WS):
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    if O[0][0]=="EC":
        #formula for the delta of a European call option given by the formula
        
        d_1=(log(S/K)+(r-d+0.5*Vol**2)*(T))/(Vol*T**0.5)
        d_2=(log(S/K)+(r-d-0.5*Vol**2)*(T))/(Vol*T**0.5)
        return exp(-d*T)*NCF(d_1)+(1/(S*Vol*(T*2*pi)**0.5))*(exp(-d*T-(d_1**2)/2)*S-K*exp(-r*T-(d_2**2)/2))
    else:
        return print("Not defined for that option")


# In[325]:


def BSVega(O,WS):
    #Calculates the vega of a European call option from formula
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    if O[0][0]=="EC":
        
        d_1=(log(S/K)+(r-d+0.5*Vol**2)*(T))/(Vol*T**0.5)
        d_2=(log(S/K)+(r-d-0.5*Vol**2)*(T))/(Vol*T**0.5)
        d_1vol=-(log(S/K)+r-d)/Vol**2+0.5*T**0.5
        d_2vol=-(log(S/K)+r-d)/Vol**2-0.5*T**0.5
        return (S*exp(-d*T-d_1**2/2)*d_1vol-K*exp(-r*T-d_2**2/2)*d_2vol)/(2*pi)**0.5
    else:
        return print("Not defined for that option")


# In[326]:


def BSRho(O,WS):
    #Calculates the rho of a European call option from formula
    r=WS[0]
    T=O[2]
    d=O[1][1]
    S=O[1][0]
    Vol=O[1][3]
    K=O[3]
    if O[0][0]=="EC":
        
        d_1=(log(S/K)+(r-d+0.5*Vol**2)*(T))/(Vol*T**0.5)
        d_2=(log(S/K)+(r-d-0.5*Vol**2)*(T))/(Vol*T**0.5)
        A=S*exp(-d*T-d_1**2/2)*T**0.5/(Vol*(2*pi)**0.5)
        B=-K*exp(-r*T)*(-T*NCF(d_2)+exp(-d_2**2/2)*T**0.5/(Vol*(2*pi)**0.5))
        return A+B
    else:
        return print("Not defined for that option")


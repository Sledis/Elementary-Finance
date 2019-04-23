#!/usr/bin/env python
# coding: utf-8

# In[36]:


#This is a collection of statistical functions that I will need.
import numpy as np
from math import log
from math import exp
from math import pi
#This function will take several lists and trim them to the same length outputting as a list of arrays. This will be important when
#calculating covariance
def Trim(*args):
    L=len(args)
    Min=len(args[0])
    for i in range(1,L):
        Min=min(Min,len(args[i]))
    I=[0]*L
    for i in range(L):
        I[i]=args[i][:Min]
        
    return I


# In[37]:


#We now create a function that will take some lists and produce a numpy array of their means.
def Means(*args):
    #We first trim all the data to be the same length.
    A=Trim(*args)
    N=len(A[0])
    Means=np.zeros(len(args))
    for i in range(len(args)):
        Means[i]=sum(A[i])/N
    return Means


# In[38]:


#We now define the covariance function of two lists
def Covar(A,B):
    #First trim all the data
    C=Trim(A,B)
    N=len(C[0])
    if N>1:
        M=Means(A,B)
        Sum=0
    
        for i in range(N):
            Sum=Sum+(C[0][i]-M[0])*(C[1][i]-M[1])
        Sum=Sum/(N-1)
        return Sum
    else:
        print("Can not calculate the covariance of 1 bit of data.")


# In[39]:


#We now create the sigma covariance matrix.
def Sigma(*args):
    l=len(args)
    Sig=np.zeros((l,l))
    for i in range(l):
        for j in range(i,l):
            Sig[i,j]=Covar(args[i],args[j])
            Sig[j,i]=Covar(args[j],args[i])
    return Sig


# In[ ]:


#The following an inverse cumulative normal function calculator.
a_0=2.50662823884
a_1=-18.61500062529
a_2=41.39119773534
a_3=-25.44106049637
b_0=-8.47350193090
b_1=23.08336743743
b_2=-21.06224101826
b_3=3.13082909833

c_0=0.3374754822726147
c_1=0.9761690190917186
c_2=0.1607979714918209
c_3=0.0276438810333863
c_4=0.0038405729373609
c_5=0.0003951896511919
c_6=0.0000321767881768
c_7=0.0000002888167364
c_8=0.0000003960315187

def ICNF(x):
    #Computes the inverse cumulative normal function of x for x in (0,1).
    #Comes fomr B.2.1 in Joshi's concepts and practices of mathematical finance.
    if x<1 and x>0:
        y=x-0.5
        if abs(y)<0.42:
            r=y**2
            A=(y*(a_0+a_1*r+a_2*r**2+a_3*r**3))/(b_0*r+b_1*r**2+b_2*r**3+b_3*r**4+1.0)
            return A
        
        if abs(y)>=0.42:
            if y<0:
                r=x
            if y>=0:
                r=1-x
        
        
            s=log(-log(r))
            t=c_0*s**0+c_1*s**1+c_2*s**2+c_3*s**3+c_4*s**4+c_5*s**5+c_6*s**6+c_7*s**7+c_8*s**8
            #page 417 says the s should be r, but this is a typo.
            if x>0.5:
                return t
            else:
                return -t
        
    else:
        print("Undefined")


# In[ ]:


#We now define a computative form of the cumulative normal function taken from page 417 of Joshi.


def LHCNF(x):
    #This computes the left hand side of the normal
    if x>0:
        k=1/(1+0.2316419*x)
        
        N=1-(1/(2*pi)**0.5)*exp(-x*x/2)*k*(0.319371530+k*(-0.356563782+k*(1.781477937+k*(-1.821255978+1.330274429*k))))
        return N
    if x==0:
        return 1/2
    else:
        return print("Undefined")
    
def NCF(x):
    if x>=0:
        return LHCNF(x)
    if x<0:
        return 1-LHCNF(-x)


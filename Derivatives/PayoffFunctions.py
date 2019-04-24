#!/usr/bin/env python
# coding: utf-8

# In[2]:


#This is a collection of all the payoff functions we will need. Seperating them out will be more relevant
#when we get to monte carlo for non-vanilla options.

def EuropeanCallPayoff(x,K):
    #The pay off of a European call of stock finishing at x with a strike of K.
    if x>K:
        return x-K
    else:
        return 0
EuropeanCallPayoff(90,100)


# In[6]:


def EuropeanPutPayoff(x,K):
    #The pay off of a European call of stock finishing at x with a strike of K.
    if x<K:
        return -x+K
    else:
        return 0


# In[2]:


def DigitalCallPayoff(x,K):
    #The pay off of a Digital call of a stock finishing at x with a strike of K.
    if x>K:
        return 1
    else:
        return 0
DigitalCallPayoff(90,100)


# In[4]:


def DigitalPutPayoff(x,K):
    #The pay off of a Digital put of a stock finishing at x with a strike of K.
    if x<K:
        return 1
    else:
        return 0
DigitalPutPayoff(80,90)


# In[ ]:





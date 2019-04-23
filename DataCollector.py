#!/usr/bin/env python
# coding: utf-8

# In[1]:


from lxml import html
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re

#This is a collection of functions that can take a Yahoo finance page and return finance information took from the website.

def CurrentPrice(url,Curr):
    #This is a simple function that will take a url from yahoo finance and output the current value
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    t=soup.find('span',{'class':'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'})
    #We now need to use regex to remove any commas if they occur.
    t = re.sub(r'[\,]+', '', t.text)

        
    
    
    #We have to scale the data in case it is stored in pounds or pence.
    Scal=1
    if Curr=="P":
        Scal=100
    

    
    return float(t)*Scal

#We now generalize the above function so that given a list of urls it will output a list of current prices.
#It takes arguements in the form of a 2d vector of a url and the currency it is valued in.
def PsFromURL(*args):
    l=len(args)
    P=np.zeros(l)
    for i in range(l):
        P[i]=CurrentPrice(args[i][0],args[i][1])
    return P


# In[2]:


def LastClosePrice(url,Curr):
    #This function will output the previous close of a stock displayed on yahoo.
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    t=soup.find('span',{'class':'Trsdu(0.3s) '})
    t = re.sub(r'[\,]+', '', t.text)
    Scal=1
    if Curr=="P":
        Scal=100

    return float(t)*Scal


def CsFromURL(*args):
    l=len(args)
    P=np.zeros(l)
    for i in range(l):
        P[i]=LastClosePrice(args[i][0],args[i][1])
    return P


# In[3]:


def SummaryToHistory(URL):
    #This takes a yahoo summary page and converts it to the history page.
    #This is to make out later code less confusing, by only needing to specify one page, instead of two.
    l=URL.find("?")
    A=URL[:l]
    B="/history"
    C=URL[l:]
    A+=B
    A+=C
    return(A)


# In[4]:


def HistoricalData(URL,Curr):
    #This function takes a url from Yahoo Finance summary page of a share and outputs it as a numpy list
    #NB that on yahoo finance, markets like the ftse100 are displayed in GBP
    #Where as the individual components are priced in pence. We shall evaluate everything in pence.
    URL=SummaryToHistory(URL)
    html=requests.get(URL).content
    df_list=pd.read_html(html)
    lis1=df_list[-2]
    j=0
    
    for i in range(len(lis1)):
        if np.isnan(lis1.iloc[i,4])==1:
            j=j+1
    PL=np.zeros(len(lis1)-j)
    #We have now collected the price list and created a zero array of equal length, minus the dividend
    #dates.

    
    Scal=1
    if Curr=="P":
        Scal=100
    #We have now set a scaling factor, so that we everything will be output in pence.    
    
    j=0

    for i in range(len(lis1)):

        if np.isnan(lis1.iloc[i,4])==0:
        

            PL[i-j]=float(lis1.iloc[i,4]*Scal)
        else:
            j=j+1
        
    #We have now generated a numpy array in pence of the historical prices and removed all dividend information.

    return PL

#We now extend the above function so that it can take a list of [stock, currecny] and output historic data in pence.

def HistoriesFromURL(*args):
    l=len(args)
    P=[]
    for i in range(l):
        P.append(HistoricalData(args[i][0],args[i][1]))
    return P


# In[5]:


def PricesToReturns(*args):
    #Takes a collection of history prcies and outputs a collection of returns prices.
    l=len(args)
    T=[]
    for i in range(l):
        A=args[i]
        m=len(A)

        R=[]
        for j in range(m-1):
            
            R.append(A[j]/A[j+1]-1)
        T.append(R)
    return T


# In[ ]:





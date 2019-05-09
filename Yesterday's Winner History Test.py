#!/usr/bin/env python
# coding: utf-8

# In[12]:


#Testing the yesterdays winner startegy over historic data creating csv files.
import numpy as np
import time
import csv
import re






# In[13]:


def Winner(*args):
    
    #Takes in a collections of CSV files and returns a list for each trading day, on each day it will leave the close value of the best performing and 0 otherwise.
    #It also provides a list of all closes. This will be needed later, so it is more optimal to take a copy of them now, then recall the csvs later.
    I=[]
    C=[]
    for arg in args:
        Doc=open(arg,"r")
        values=csv.reader(Doc)
        DayChange=[]
        Close=[]
        for row in values:
    
            if re.match('^[0-9\.]*$',row[4]) and re.match('^[0-9\.]*$',row[1]):
                DayChange.append(float(row[4])/float(row[1]))
                Close.append(float(row[4]))
        I.append(DayChange)
        C.append(Close)
        
    Closes=[0]*len(I[0])
    for i in range(len(I[0])-1):
        Cha=[0]*len(args)
        for j in range(len(args)):
            Cha[j]=C[j][i]
        Closes[i]=Cha
        
        
    Port=[0]*len(I[0])
    for i in range(len(I[0])-1):
        M=float("-inf")
        Values=[0]*len(args)
        for j in range(len(args)):
            
            if I[j][i]>M:
                M=I[j][i]
                J=j
        Values[J]=C[J][i]
        Port[i]=Values
        
    
    return [Port,Closes]


# In[14]:


def Portfollio(Cash,*args):
    #This takes a starting value of cash and csv files and produces the "yesterdays winner strategy" to produce the portfollios it would have produced and tracks the cash value.
    W=Winner(*args)[0]
    N=len(W)
    DayHold=[0]*len(args)
    P=[]
    for j in range(len(W[0])):
        if W[0][j]!=0:
            DayHold[j]=Cash/W[0][j]
            
    P.append(DayHold)
    
    Closes=Winner(*args)[1]
    C=[Cash]
    for i in range(1,N-1):
    
        Cash=np.dot(Closes[i],P[i-1])
        DayHold=[0]*len(args)
        C.append(Cash)
        for j in range(len(W[i])):
            if W[i][j]!=0:
                DayHold[j]=Cash/W[i][j]
        P.append(DayHold)
    return [P,C]


# In[27]:


def YWTest(Name,Histories,Cash):
    Doc="D:\My Documents\GitHub\Elementary-Finance\Yesterdays Winner Tests\\"
    Doc+=Name
    Doc+=".csv"
    w=open(Doc, "w")
    writeFile=csv.writer(w)
    A=Portfollio(Cash,*Histories)
    P=A[0]
    Cash=A[1]
    for i in range(len(P)):
        P[i].append(Cash[i])
    
        writeFile.writerow(P[i])
    
    


# In[55]:


Histories1=["D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\BARC.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\HSBC.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\LLOY.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\RBS.csv"]


# In[56]:


YWTest("Barc,HSBC,LLo,RBS",Histories1,100)


# In[57]:


Histories2=["D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\BATS.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\BP.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\HL.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\MKS.L.csv"]


# In[58]:


YWTest("BAT,BP,HL,MKS",Histories2,100)


# In[59]:


Histories3=["D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\BARC.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\HSBC.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\LLOY.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\8-5-19\RBS.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\BATS.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\BP.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\HL.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\MKS.L.csv"]


# In[60]:


YWTest("BAT,BP,HL,MKS,Big4",Histories3,100)


# In[61]:


Histories4=["D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\SBRY.L.csv","D:\My Documents\GitHub\Elementary-Finance\csvs\9-5-19\TSCO.L.csv"]


# In[62]:


YWTest("SBRY,TSCO",Histories4,100)


#!/usr/bin/env python
# coding: utf-8

# In[9]:


#This caclulates portfollios to reblanace once a day based on the CER model. It will run on several 
#portfollios with a starting cash value of 10000p and the data will be stored at 
#https://docs.google.com/spreadsheets/d/1V4-ibttRKCvFJyOrqVu6AIjGC0FWr7Qb8kB0lq6e7tk/edit#gid=1370185696

#At 6pm each day this code will initialize, checking if the following day is a trading day.
#if it is, it will use historical data to calculate the CER portfollio and how much it's portfollio is worth at the close
#of today.

#it assumes you buy that portfollio at the open tomorrow morning after instantly selling your current portfollio at open.

#assumptions
#no dividends
#no trading fees
#open and close prices are the same and instant trade is possible
#there is no riskless interest rate (to be added into another program.)
import numpy as np
import sys
import re


sys.path.insert(0, 'D:\My Documents\GitHub\Elementary-Finance')
import DataCollector as DC
from FinancialStats import Sigma
from FinancialStats import Means
from HolidayLogic import BanksOpen
from HolidayLogic import UK2019
import datetime


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def MinPort(Exp,*args):
    #This takes an expected target and a colleciton of historical price lists and uses the CER model to produce a portfollio
    #from the given stocks with that expected return and minimum variance.
    l=len(args)
    b=np.zeros(l+2)
    Mean=Means(*args)
    
    Sig=Sigma(*args)

    #We define the vector b as given by page 12 of http://faculty.washington.edu/ezivot/econ424/portfolioTheoryMatrix.pdf
    b[l]=Exp
    b[l+1]=1

    #We now define the A matrix
    A=np.zeros((l+2,l+2))
    for i in range(l):
        for j in range(l):
            A[i,j]=2*Sig[i,j]

    for i in range(l):
        A[l,i]=Mean[i]
        A[i,l]=Mean[i]
        A[l+1,i]=1
        A[i,l+1]=1
    
   
    Port=np.dot(np.linalg.inv(A),b)[:l]
    ER=np.dot(Port,Mean)
    Var=np.dot(Port,np.dot(Sig,Port))
   
    print("Expected return is", ER, "with variance", Var)
    return Port
   


# In[10]:


#We will need a function that can take our current portfollio and evaluate it's value.
def PortValue(*args):
    #This function returns the current value of all holdings.
    P=DC.PsFromURL(*args)
    
    ValueVec=np.ones(len(args)+1)
   
    for i in range(len(args)):
        ValueVec[i]=P[i]
    
    col_len = len(ws.col_values(1))
    vect=np.array(ws.row_values(col_len)[1:len(args)+2])
    
    Amount=[float(i) for i in vect]
    
    Cash=np.dot(ValueVec,Amount)
    return Cash


# In[11]:


#We now combine these to update the spreadsheet

def SheetUpdate(Exp,*args):
    #We first start by checking that tomorrow's values haven't already been caluclated. As this is a one trade per day strat.
    #Otherwise it will just add another row to the spreadsheet.
    col_len = len(ws.col_values(1))
    tomorrow =  datetime.date.today() + datetime.timedelta(days=1)
    l=len(args)
    
    if ws.cell(col_len,1).value==tomorrow.strftime("%d/%m/%Y"):
        #If tomorrows value has already been calculated, delete it and recalculate
        #This allows, for example, us to test during the day and then when it properly evaluates at the end of the day,
        #it will over-write our test (incorrect data).
        ws.delete_row(col_len)
        col_len = len(ws.col_values(1))
    ValueAtClose=PortValue(*args)
    ws.update_cell(col_len,l+3,ValueAtClose)  
    if BanksOpen(UK2019,tomorrow)==1:      
        

        
        CurrentPrice=DC.PsFromURL(*args)
        #First we calculate how much money we currently have
        
        Histories=DC.HistoriesFromURL(*args)
        Returns=DC.PricesToReturns(*Histories)
        A=MinPort((1+Exp)**(1/260)-1,*Returns)
        #here we have calculated the portfollio that we should buy at the begining of trading the next day, and the value that 
        #We get from selling our current portfollio.
        
        #Each element in A only tells us what percentage of our portfollio should go on each stock.
        C=np.zeros(l)
        for i in range(l):
            C[i]=ValueAtClose*A[i]/CurrentPrice[i]
        
        
        
        
    

        
        B = [tomorrow.strftime("%d/%m/%Y")]
        B.extend(C)
        B.extend([0])
        ws.insert_row(B, col_len+1)


# In[12]:


#We now intialize the spreadsheet and start buldining naively portfollios to see how it will trade them in the coming months.
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

ss = client.open('CERV1')


# In[13]:


#Big4
Barc=['https://uk.finance.yahoo.com/quote/BARC.L?p=BARC.L','p']
HSBC=['https://uk.finance.yahoo.com/quote/HSBA.L?p=HSBA.L','p']
Llo=['https://uk.finance.yahoo.com/quote/LLOY.L?p=LLOY.L','p']
RBS=['https://uk.finance.yahoo.com/quote/RBS.L?p=RBS.L','p']
Big4=[Barc,HSBC,Llo,RBS]
ws = ss.worksheet("Big4")
SheetUpdate(0.01,*Big4)


# In[14]:


#Chens
ITV=["https://uk.finance.yahoo.com/quote/ITV.L?p=ITV.L",'p']
JustEat=["https://uk.finance.yahoo.com/quote/JE.L?p=JE.L",'p']
Tesco=["https://uk.finance.yahoo.com/quote/TSCO.L?p=TSCO.L",'p']
Vodafone=["https://uk.finance.yahoo.com/quote/VOD.L?p=VOD.L",'p']
chen=[ITV,JustEat,Tesco,Vodafone]
ws=ss.worksheet("Chen")
SheetUpdate(0.12,*chen)


# In[15]:


#Sams
BP=["https://uk.finance.yahoo.com/quote/BP.L?p=BP.L",'p']
Sainsbury=["https://uk.finance.yahoo.com/quote/SBRY.L?p=SBRY.L",'p']
MS=["https://uk.finance.yahoo.com/quote/MKS.L?p=MKS.L",'p']
Uni=["https://uk.finance.yahoo.com/quote/ULVR.L?p=ULVR.L",'p']
sam=[BP,Sainsbury,MS,Uni]
ws=ss.worksheet("Sam")
SheetUpdate(0.03,*sam)


# In[16]:


#James
Tobacco=['https://uk.finance.yahoo.com/quote/BATS.L?p=BATS.L',"p"]
james=[Sainsbury,Tobacco]
ws=ss.worksheet("James")
SheetUpdate(0.045,*james)


# In[ ]:





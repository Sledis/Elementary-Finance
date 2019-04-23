#!/usr/bin/env python
# coding: utf-8

# In[2]:


#This will implement a trading strategy applied at the open every morning. It will sell all its portfollio and use that money
#to exclusively buy the share that performed best yesterday. You always bet on yesterdays winner. It will be run everynight afterclose

from DataCollector import CurrentPrice
from DataCollector import LastClosePrice
from HolidayLogic import BanksOpen
from HolidayLogic import UK2019
import datetime
import numpy as np

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def Winner(*args):
    #This function will look at all the urls given, determine which one performed the best today, then output an array
    #with zeros in all the "underperforming" stocks and the current price of that stock.
    l=len(args)
    Max=-1
    #Any negative value works here.
    J=0
    for i in range(l):
        change=CurrentPrice(args[i][0],args[i][1])/LastClosePrice(args[i][0],args[i][1])
        
        if change>Max:
            Max=change
            J=i
    Portfollio=np.zeros(l)
    Portfollio[J]=CurrentPrice(args[J][0],args[J][1])
    return Portfollio



# In[3]:


#We now define a function that will calculate how much money we have at the end of the day
def PortfollioValue(*args):
    #This function returns the current value of all holdings.
    l=len(args)
    Prices=np.zeros(l+1)
    for i in range(l):
        Prices[i]=float(CurrentPrice(args[i][0],args[i][1]))
    Prices[l]=1
    col_len = len(ws.col_values(1))
    vect=np.array(ws.row_values(col_len)[1:l+2])
    Amount=[float(i) for i in vect]
    
    Cash=np.dot(Prices,Amount)
    return Cash


# In[4]:


def NewPortfollio(*args):
    #With the above functions we now know how much money we have, what we need to buy and the price, so we easily derive tomorrows portfollio
    P=PortfollioValue(*args)
    W=Winner(*args)
    Portfollio=np.zeros(len(args))
    for i in range(len(args)):
        if W[i]!=0:
            Portfollio[i]=P/W[i]
    return Portfollio


# In[5]:


#We now combine these to update the spreadsheet

def SheetUpdate(*args):
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

        
    if BanksOpen(UK2019,tomorrow)==1:        
        A=NewPortfollio(*args)
        
        ValueAtClose=PortfollioValue(*args)
        
        #here we have calculated the portfollio that we should buy at the begining of trading the next day, and the value that 
        #We get from selling our current portfollio.
        ws.update_cell(col_len,l+3,ValueAtClose)
    

        
        B = [tomorrow.strftime("%d/%m/%Y")]
        B.extend(A)
        B.extend([0])
        ws.insert_row(B, col_len+1)


# In[6]:


#I now pick the following 4 stocks of the big 4 british banks.
a=["https://uk.finance.yahoo.com/quote/BARC.L?p=BARC.L",'p']
b=["https://uk.finance.yahoo.com/quote/HSBA.L?p=HSBA.L",'p']
c=["https://uk.finance.yahoo.com/quote/LLOY.L?p=LLOY.L",'p']
d=["https://uk.finance.yahoo.com/quote/RBS.L?p=RBS.L",'p']


# In[9]:


#This block of code initalizes the code accessing the google sheet of historic trades and cash value

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

ss = client.open('YesterdaysWinner')
ws = ss.worksheet("Sheet1")


# In[10]:


SheetUpdate(a,b,c,d)


# In[20]:





# In[ ]:





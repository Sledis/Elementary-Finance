#!/usr/bin/env python
# coding: utf-8

# In[1]:


#This is a collection of functions that deal with determining if banks are open.
import datetime

#Collection of bankholidays
UK2019=["01/01/2019","17/03/2019","19/04/2019","22/04/2019","06/05/2019","27/05/2019","12/07/2019","26/08/2019","25/12/2019","26/12/2019"]
#The UK bank holidays for 2019.
def BanksOpen(B,Date):
    #This program determines if banks in a country are open to trade in 2019.
    # It returns 0 if banks are closed tomorrow. And 1 if they are open.
    #It does this by checking if tomorrow is a weekend or a bank holiday.
    if Date.strftime("%Y")=='2019':

        d1 = Date.strftime("%d/%m/%Y")
        wkday=Date.weekday()
        
        if wkday in [5,6]:
            return 0
        elif d1 in B:
            return 0
        else:
            return 1
    else:
        return print("This code is only available during 2019, until the bankholiday data has been updated.")


# In[ ]:





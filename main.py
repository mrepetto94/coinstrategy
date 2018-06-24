import krakenex
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from statsmodels.tsa.stattools import adfuller

pair = 'XBTEUR'

k = krakenex.API(key=os.environ['KRAKENKEY'],
                 secret=os.environ['KRAKENSECRET'])

ret = k.query_public('Trades', data = {'pair': pair})

ret = ret['result']['XXBTZEUR']

df = pd.DataFrame(ret,
                  columns = ['Price', 'Volume', 'Time', 'BS', 'ML', 'Misc'])

df.Price = pd.to_numeric(df.Price)
df.Time = pd.to_datetime(df.Time, unit ='s')

#split the df in training and testing
df_training =df.iloc[:799,:]
df_testing = df.iloc[800:,:]


###Backtesting###
#i = 1
#test = []
#pvalue = []
# result = []
#l = 250
#while i<=(999-l) :
#    result = adfuller(df.Price[i:(i+l)], autolag = 't-stat')
#`    test.append(result[0])
#   pvalue.append(result[1])
#    i+=1

#Calculate the hedgeratio
df["HedgeRatio"] =  (df.Price -df.Price.mean())/df.Price.std()
df.HedgeRatio = df.HedgeRatio / max(abs(df.HedgeRatio))
df.HedgeRatio = (-1) * df.HedgeRatio

i = 0
portfolio = [1,0]
pnl = []
while i <= 998:
    if df.HedgeRatio[i] >= 0 :
        portfolio[1] = portfolio[1] + ((portfolio[0]/df.Price[i])*df.HedgeRatio[i])
        portfolio[0] = portfolio[0] * (1-df.HedgeRatio[i])
        print("BUY")
    else:
        portfolio[0] = portfolio [0] + ((portfolio[1]*df.Price[i])*(abs(df.HedgeRatio[1])))
        portfolio[1] = portfolio[1] * (1-abs(df.HedgeRatio[i]))
        print("SELL")
    pnl.append(portfolio[0] + portfolio[1]*df.Price[i])
    time.sleep(0.2)
    i+=1



###Backtesting a random strategy###


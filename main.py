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

###Backtesting###

i = 1
test = []
pvalue = []
result = []
l = 250
while i<=(999-l) :
    result = adfuller(df.Price[i:(i+l)], autolag = 't-stat')
    test.append(result[0])
    pvalue.append(result[1])
    i+=1

#plot1= plt.subplot2grid((3,1),(0,0))
#plot1.plot(df.Price)
#plot2= plt.subplot2grid((3,1),(1,0))
#plot2.plot(test)
#plot3= plt.subplot2grid((3,1),(2,0))
#plot3.plot(pvalue)
#plt.show()

###Backtesting a random strategy###
i = 1
store = 0
profit = []
while i<=999 :
    if store > 0 :

        if random.random() >= 0.5 :
            pl = df.Price[i] - store
            store = 0
            profit.append(pl)
    else:
        if random.random() >= 0.5 :
            store = df.Price[i]
    i += 1

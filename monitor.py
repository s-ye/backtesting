#print some graphs to a folder called monitor


# Ensure required packages are installed
required_packages = [
    "matplotlib",
    "numpy",
    "pandas",
    "seaborn",
    "yfinance"
]

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import yfinance as yf
import datetime
from datetime import timedelta
import strategies as s
import staticvariables as sv

def applyStrategy(hist, strategy):
    rsiparams = (10000,.8,20)
    averagedownparams = (10000,.8,.5,10)
    if strategy == 'rsi':
        return s.rsifactor(hist,rsiparams,True)
    elif strategy == 'mac':
        return s.rsifactor(hist,rsiparams,False)
    elif strategy == 'avgdown':
        return s.averageDown(hist,averagedownparams)
    
def write(
    total, winning_trades, losing_trades, length_of_trades, buy, sell, stock, strat
):
    
    with open('/Users/songye03/Desktop/backtesting/monitor/overview_' + strat + '.txt', 'a') as f:
        # if no trades were made, skip the stock
        # write the current time up to minutes
        f.write(str(today) + '\n')
        if len(buy) == 0:
            f.write(stock + ' no trades made\n\n')
            return
        invest = (total - 10000)/100
        close = hist['Close']
        fig = plt.figure(figsize = (15,5))
        plt.plot(close, color='r', lw=2.)
        plt.plot(close, '^', markersize=10, color='m', label = 'buying signal', markevery = buy)
        plt.plot(close, 'v', markersize=10, color='k', label = 'selling signal', markevery = sell)
        plt.plot(hist.index, hist["SMA_50"], color='g', lw=1., label='SMA 50')
        plt.plot(hist.index, hist["SMA_200"], color='b', lw=1., label='SMA 200')
        # plt.plot(hist.index, hist["RSI"], color='b', lw=1., label='RSI')
        plt.title('net %f, total profit %f%%'%(total, invest))
        plt.legend()

        path = name +"/" + stock + strat + '.png'
        fig.savefig(path)
        plt.close(fig)
        # write to overview.txt
        
        f.write(stock + ' value of portfolio %f, total return %f%%\n'%(total, invest))
        # check if the last action was a buy or sell
        if len(sell) == 0 or buy[-1] > sell[-1]:
            f.write('last action: buy at ')
            datetime = hist.index[buy[-1]]
            f.write(str(datetime.date()))

            if datetime.date() == hist.index[-1].date():
                buysignaltoday[stock] = True


            f.write(' at price: %f\n'%hist.Close[datetime])
            # # how many shares were bought at the last buy
            # f.write("each currently worth: %f\n"%hist.Close[-1])
            # f.write("total worth of shares and cash: %f\n"%total)
        else:
            f.write('last action: sell on ')
            datetime = hist.index[sell[-1]]
            f.write(str(datetime.date()))
            if datetime.date() == hist.index[-1].date():
                sellsignaltoday[stock] = True
            f.write(' at price: %f\n'%hist.Close[datetime])


        average_len = sum(length_of_trades, timedelta(0)) / len(length_of_trades) if len(length_of_trades) > 0 else timedelta(0)
        f.write("average length of trades: %s\n"%str(average_len))
        f.write("winning trades: %d\n"%len(winning_trades))
        f.write("losing trades: %d\n"%len(losing_trades))
        f.write('\n')
    


lastbuy = {}

buysignaltoday = {stock: False for stock in sv.stocks}
sellsignaltoday = {stock: False for stock in sv.stocks}

today = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
name = 'monitor'

# Create a folder called monitor
if not os.path.exists(name):
    os.makedirs(name)

for strat in sv.strats:
    for stock in sv.stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="2y", interval="1h")
        hist = sv.processHist(hist)

        
        total, winning_trades, losing_trades, length_of_trades, buy, sell = applyStrategy(hist, strat)
        
        write(total, winning_trades, losing_trades, length_of_trades, buy, sell, stock, strat)
        



#if any of the signals were today, write to a file
for stock in sv.stocks:
    if buysignaltoday[stock] or sellsignaltoday[stock]:
        with open('/Users/songye03/Desktop/backtesting/signals.txt', 'w') as f:
            f.write(stock)


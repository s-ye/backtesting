#print some graphs to a folder called monitor
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import yfinance as yf
import datetime
from datetime import timedelta
import strategies as s

def applyStrategy(hist, strategy):
    if strategy == 'rsi':
        return s.rsifactor(hist,True)
    elif strategy == 'mac':
        return s.rsifactor(hist,False)
    
def write(
    total, winning_trades, losing_trades, length_of_trades, buy, sell, stock, strat
):
    # if no trades were made, skip the stock
    
    with open(name + '/' + 'overview_' + strat + '.txt', 'a') as f:
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
        
        f.write(stock + ' total gains %f, total investment %f%%\n'%(total, invest))
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
stocks = ['NVDA','NVO','CPNG', 'QCOM', 'INTC', 'UAL']
strats = ['rsi', 'mac']
buysignaltoday = {stock: False for stock in stocks}
sellsignaltoday = {stock: False for stock in stocks}

today = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
name = 'monitor'

# Create a folder called monitor
if not os.path.exists(name):
    os.makedirs(name)

for strat in strats:
    for stock in stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="2y", interval="1h")
        hist["Close"] = hist["Close"].astype(float)
        hist["Volume"] = hist["Volume"].astype(float)
        hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
        hist["SMA_200"] = hist["Close"].rolling(window=200).mean()
        hist["RSI"] = np.nan

        for i in range(1, len(hist)):
        # compute the RSI factor at this point
        # we will use a 14 day period
        # we will use the closing price
        # we will use the average gain and average loss
        # to calculate the RSI
            average_gain = 0
            average_loss = 0
            for j in range(1,15):
                if hist["Close"].iloc[i-j] > hist["Close"].iloc[i-j-1]:
                    average_gain += hist["Close"].iloc[i-j] - hist["Close"].iloc[i-j-1]
                else:
                    average_loss += hist["Close"].iloc[i-j-1] - hist["Close"].iloc[i-j]
            average_gain /= 14
            average_loss /= 14
            if average_loss == 0:
                hist.loc[hist.index[i], "RSI"] = 100
                continue
            RS = average_gain / average_loss
            RSI = 100 - 100/(1 + RS)
            hist.loc[hist.index[i], "RSI"] = RSI

        
        total, winning_trades, losing_trades, length_of_trades, buy, sell = applyStrategy(hist, strat)
        
        write(total, winning_trades, losing_trades, length_of_trades, buy, sell, stock, strat)
        



#if any of the signals were today, write to a file
for stock in stocks:
    if buysignaltoday[stock] or sellsignaltoday[stock]:
        with open('signals.txt', 'w') as f:
            f.write(stock)


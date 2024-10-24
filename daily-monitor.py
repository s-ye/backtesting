#print some graphs to a folder called monitor
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import yfinance as yf
import buystock as bs

lastbuy = {}
buysignaltoday = {}
sellsignaltoday = {}


# Create a folder called monitor
if not os.path.exists('monitor'):
    os.makedirs('monitor')

with open('monitor/overview.txt', 'w') as f:
    for stock in ['NVDA','NVO','CPNG', 'QCOM', 'INTC', 'UAL']:
        ticker = yf.Ticker(stock)
        df = ticker.history(period="1y", interval="1h")
        total, winning_trades, losing_trades, average_len, buy, sell = bs.buy_stock(df)

        # if no trades were made, skip the stock
        if len(buy) == 0:
            f.write(stock + ' no trades made\n\n')
            continue

        invest = (total - 10000)/100

        close = df['Close']
        fig = plt.figure(figsize = (15,5))
        plt.plot(close, color='r', lw=2.)
        plt.plot(close, '^', markersize=10, color='m', label = 'buying signal', markevery = buy)
        plt.plot(close, 'v', markersize=10, color='k', label = 'selling signal', markevery = sell)
        plt.title('net %f, total profit %f%%'%(total, invest))
        plt.legend()

        path = 'monitor/' + stock + '.png'
        fig.savefig(path)
        # write to overview.txt
        
        f.write(stock + ' total gains %f, total investment %f%%\n'%(total, invest))
        # check if the last action was a buy or sell
        if buy[-1] > sell[-1]:
            f.write('last action: buy at ')
            datetime = df.index[buy[-1]]
            f.write(str(datetime.date()))

            if datetime.date() == df.index[-1].date():
                buysignaltoday[stock] = True

            f.write(' at price: %f\n'%df.Close[datetime])
            # # how many shares were bought at the last buy
            # f.write("each currently worth: %f\n"%df.Close[-1])
            # f.write("total worth of shares and cash: %f\n"%total)
        else:
            f.write('last action: sell on ')
            f.write(str(df.index[sell[-1]].date()) + '\n')

        f.write("average length of trades: %s\n"%str(average_len))
        f.write("winning trades: %d\n"%winning_trades)
        f.write("losing trades: %d\n"%losing_trades)
        f.write('\n')
        print(buy)
        print(sell)





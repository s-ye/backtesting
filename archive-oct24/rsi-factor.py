#I want to look at a strategy that involves placing higher frequency trades. This 
#might require a different techincal indicator.
# RSI index or perhaps volatility index

from datetime import timedelta
import random

def rsifactor(hist,cash,risk):
    # we implement the moving average strategy with RSI informed trades
    # we will use a 14 day window for the RSI
    shares = 0
    previous_buy_price = 0
    previous_buy_date = hist.index[0]


    losing_trades = []
    winning_trades = []

    buy = []
    sell = []
    length_of_trades = []
    # we will spend risk percent of the portfolio on each buy
    for i in range(15, len(hist)):
        if hist["RSI_14"].iloc[i] < 30:
            if hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]:
                print("cash" + str(cash))
                print("risk" + str(risk))
                amount_to_invest = cash * risk
                print("Buy " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
                shares += amount_to_invest / hist["Close"].iloc[i]
                cash -= amount_to_invest
                previous_buy_price = hist["Close"].iloc[i]
                previous_buy_date = hist.index[i]
                buy.append(i)
        elif hist["RSI_14"].iloc[i] > 70:
            if hist["SMA_50"].iloc[i] < hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] > hist["SMA_200"].iloc[i-1] and shares > 0:
                amount_to_sell = shares * hist["Close"].iloc[i]
                sell.append(i)
                print("Sell " + str(amount_to_sell) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
                print("Profit: " + str(amount_to_sell - previous_buy_price * shares))
                print("Length of trade: " + str(hist.index[i] - previous_buy_date))
                print("\n")
                cash += amount_to_sell
                if amount_to_sell - previous_buy_price * shares > 0:
                    winning_trades.append(i)
                else:
                    losing_trades.append(i)
                length_of_trades.append(hist.index[i] - previous_buy_date)
                shares = 0
    averagelen = sum(length_of_trades, timedelta(0)) / len(length_of_trades) if len(length_of_trades) > 0 else timedelta(0)
    return cash + shares * hist["Close"].iloc[-1], winning_trades, losing_trades, length_of_trades, buy, sell

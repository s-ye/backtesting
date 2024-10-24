from datetime import timedelta
import random

def moving_average_crossover(hist, cash, risk):
    shares = 0
    previous_buy_price = 0
    previous_buy_date = hist.index[0]

    losing_trades = 0
    winning_trades = 0
    buy = []
    sell = []
    length_of_trades = []
    # we will spend risk percent of the portfolio on each buy
    for i in range(1, len(hist)):
        # if the short term moving average crosses above the long term moving average, buy
        if hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]:
            amount_to_invest = cash * risk
            print("Buy " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
            shares += amount_to_invest / hist["Close"].iloc[i]
            cash -= amount_to_invest
            previous_buy_price = hist["Close"].iloc[i]
            previous_buy_date = hist.index[i]
            buy.append(i)
        elif hist["SMA_50"].iloc[i] < hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] > hist["SMA_200"].iloc[i-1] and shares > 0:
            amount_to_sell = shares * hist["Close"].iloc[i]
            sell.append(i)
            print("Sell " + str(amount_to_sell) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
            print("Profit: " + str(amount_to_sell - previous_buy_price * shares))
            print("Length of trade: " + str(hist.index[i] - previous_buy_date))
            print("\n")
            cash += amount_to_sell
            if amount_to_sell - previous_buy_price * shares > 0:
                winning_trades += 1
            else:
                losing_trades += 1
            length_of_trades.append(hist.index[i] - previous_buy_date)
            shares = 0
    # print("Cash: " + str(cash))
    # print("Shares: " + str(shares))
    # print("Total: " + str(cash + shares * hist["Close"].iloc[-1]))
    # print("Winning trades: " + str(winning_trades))
    # print("Losing trades: " + str(losing_trades))
    averagelen = sum(length_of_trades, timedelta(0)) / len(length_of_trades) if len(length_of_trades) > 0 else timedelta(0)
    # print("Average length of trades: " + str(averagelen))
    return cash + shares * hist["Close"].iloc[-1], winning_trades, losing_trades, averagelen, buy, sell

def moving_average_crossover_with_random_threshold(hist, cash,risk):
    shares = 0
    previous_buy_price = 0
    previous_buy_date = hist.index[0]

    losing_trades = 0
    winning_trades = 0
    length_of_trades = []
    # we will spend risk percent of the portfolio on each buy
    
    alpha = random.uniform(-0.07, 0.07)
    for i in range(1, len(hist)):
        if (1+alpha)*hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and (1+alpha)*hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]:
            amount_to_invest = cash * risk
            # print("Buy " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
            shares += amount_to_invest / hist["Close"].iloc[i]
            cash -= amount_to_invest
            previous_buy_price = hist["Close"].iloc[i]
            previous_buy_date = hist.index[i]
        elif (1+alpha)*hist["SMA_50"].iloc[i] < hist["SMA_200"].iloc[i] and (1+alpha)*hist["SMA_50"].iloc[i-1] > hist["SMA_200"].iloc[i-1]:
            amount_to_sell = shares * hist["Close"].iloc[i]
            # print("Sell " + str(amount_to_sell) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
            # print("Profit: " + str(amount_to_sell - previous_buy_price * shares))
            # print("Length of trade: " + str(hist.index[i] - previous_buy_date))
            # print("\n")
            cash += amount_to_sell
            if amount_to_sell - previous_buy_price * shares > 0:
                winning_trades += 1
            else:
                losing_trades += 1
            length_of_trades.append(hist.index[i] - previous_buy_date)
            shares = 0
    # print("Cash: " + str(cash))
    # print("Shares: " + str(shares))
    total = cash + shares * hist["Close"].iloc[-1]
    # print("Total: " + str(total))
    # print("Winning trades: " + str(winning_trades))
    # print("Losing trades: " + str(losing_trades))
    # print("Average length of trades: " + str(sum(length_of_trades, timedelta(0)) / len(length_of_trades)))
    # print("Alpha: " + str(alpha))
    return total, winning_trades, losing_trades, sum(length_of_trades, timedelta(0)) / len(length_of_trades), alpha

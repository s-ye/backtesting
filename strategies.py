from datetime import timedelta


# A strategy is something which accepts a pandas datafram hist
# and returns a tuple of the form:
# (cash, winning_trades, losing_trades, length_of_trades, buy, sell)
# where cash is the amount of money the strategy has at the end of the backtest,
# winning_trades is the index of the trades that made money, losing_trades is the index of the trades that lost money,
# average_length_of_trades is the average length of the trades, buy is the index of the trades where the strategy bought,
# length_of_trades[i] is the length of the ith trade, 
# buy is the index of the trades where the strategy bought, and sell is the index of the trades where the strategy sold.


# moving average crossover with rsi factor
def rsifactor(hist, rsiparams, with_rsi):
    # we implement the moving average strategy with RSI informed trades
    # we will use a 14 day window for the RSI
    shares = 0
    previous_buy_price = 0
    previous_buy_date = hist.index[0]
    cash, risk, relax = rsiparams
    print("Cash, risk, relax")
    print(cash, risk, relax)

    losing_trades = []
    winning_trades = []

    buy = []
    sell = []
    length_of_trades = []
    # we will spend risk percent of the portfolio on each buy
    for i in range(15, len(hist)):
        if not with_rsi:
            if hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]:
                amount_to_invest = cash * risk
                print("Buy " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
                shares += amount_to_invest / hist["Close"].iloc[i]
                cash -= amount_to_invest
                previous_buy_price = hist["Close"].iloc[i]
                previous_buy_date = hist.index[i]
                buy.append(i)
        if not with_rsi:
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
        if with_rsi and hist["RSI"].iloc[i] < 30 + relax and hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]:
            amount_to_invest = cash * risk
            print("Buy " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
            shares += amount_to_invest / hist["Close"].iloc[i]
            cash -= amount_to_invest
            previous_buy_price = hist["Close"].iloc[i]
            previous_buy_date = hist.index[i]
            buy.append(i)
        if with_rsi and hist["RSI"].iloc[i] > 70 - relax and hist["SMA_50"].iloc[i] < hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] > hist["SMA_200"].iloc[i-1] and shares > 0:
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

# when the stock moves against us and the moving average is still above the 200 day moving average and the RSI is below 30, we will buy more shares
def averageDown(hist, averagedownparams):
    shares = 0
    previous_buy_price = 0
    previous_buy_date = hist.index[0]
    cash, risk, addon, reevaluate = averagedownparams

    losing_trades = []
    winning_trades = []

    buy = []
    sell = []
    length_of_trades = []
    # we will spend risk percent of the portfolio on each initial buy,
    # using moving average crossover strategy
    # and reevaluate our strategy after reevaluate days

    # if the stock moved against us and the RSI is below 30, we will buy more shares
    # spending addon percent of the portfolio

    # our exit strategy remains the same as the moving average crossover strategy
    for i in range(15, len(hist)):
        if hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]:
            amount_to_invest = cash * risk
            print("Initial buy " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
            shares += amount_to_invest / hist["Close"].iloc[i]
            cash -= amount_to_invest
            previous_buy_price = hist["Close"].iloc[i]
            previous_buy_date = hist.index[i]
            buy.append(i)
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
        if i % reevaluate == 0 and len(buy) > 0 and shares > 0:
            previous_buy_price = hist["Close"].iloc[buy[-1]]
            current_price = hist["Close"].iloc[i]
            if current_price < previous_buy_price and hist["RSI"].iloc[i] < 30:
                amount_to_invest = cash * addon
                print("Add on " + str(amount_to_invest) + " dollars worth of shares at " + str(hist["Close"].iloc[i]) + " " + str(hist.index[i]))
                shares += amount_to_invest / hist["Close"].iloc[i]
                cash -= amount_to_invest
                previous_buy_price = hist["Close"].iloc[i]
                previous_buy_date = hist.index[i]
                buy.append(i)

    return cash + shares * hist["Close"].iloc[-1], winning_trades, losing_trades, length_of_trades, buy, sell



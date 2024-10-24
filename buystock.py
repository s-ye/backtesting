import yfinance as yf
import pandas as pd
import moving_average_crossover as mac
import matplotlib.pyplot as plt



def buy_stock(hist):
    hist["Close"] = hist["Close"].astype(float)
    hist["Volume"] = hist["Volume"].astype(float)
    hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
    hist["SMA_200"] = hist["Close"].rolling(window=200).mean()
    cash = 10000
    risk = 0.8
    total, winning_trades, losing_trades, average_len, buy, sell = mac.moving_average_crossover(hist, cash, risk)
    return total, winning_trades, losing_trades, average_len, buy, sell

# hist = intc.history(period="max")
# # hist is a pandas DataFrame
# # we introduce methods to help us better interact with the data
# # in particular we need summary statistics and moving averages
# # we will also need to be able to access
# # the data in a way that is useful for our backtesting

# # first we need to get the time series data and the closing prices and the volume
# # from this, we can calculate the moving averages

# hist["Close"] = hist["Close"].astype(float)
# hist["Volume"] = hist["Volume"].astype(float)

# # we will also need to calculate the moving averages
# hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
# hist["SMA_200"] = hist["Close"].rolling(window=200).mean()

#print all the moving averages with volume and closing prices
# print(hist[["Close", "Volume", "SMA_50", "SMA_200"]].tail(20))


# opt = intc.option_chain("2024-12-20")
# #show the columns of the option chain
# print(opt.calls.columns)
# print(opt.calls["openInterest"])

# # the scraping is not working as expected for the option chain
# # but this can be remedied by looping through all the option tickers
# # and extracting the data for each one
# # we can only get the price of an option, no further information

# intccall = yf.Ticker("INTC241220C00032000")
# print(intccall.info)
# intccallhist = intccall.history(period="max")



# now we begin to implement the backtesting strategy
# we will need to define the strategy and the rules for entering and exiting positions
# then we will assume that we start with 10000 USD and start trading over the course of 1 year
# looking at daily data. At the end of the year, we will calculate the profit and loss.

# our backtesting strategy will be a simple moving average crossover strategy
# we will buy when the short term moving average crosses above the long term moving average
# and sell when the short term moving average crosses below the long term moving average

# we will also need to calculate the profit and loss of the strategy
# we will need to calculate the profit and loss of each trade
# and the overall profit and loss of the strategy


# cash = 10000
# shares = 0
# risk = 0.8
# we will spend 10 percent of the portfolio on each buy



# profit = mac.moving_average_crossover(hist, cash, risk)
# thereturn = (profit - cash) / cash


# # Assuming risk is a list of different risk levels and thereturn is a list of corresponding returns
# risk_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# returns = []

# for risk in risk_levels:
#     profit = mac.moving_average_crossover(hist, cash, risk)
#     thereturn = (profit - cash) / cash
#     returns.append(thereturn)

# plt.plot(risk_levels, returns, marker='o')
# plt.xlabel('Risk Level')
# plt.ylabel('Return')
# plt.title('Return vs Risk Level')
# plt.grid(True)
# plt.show()

# random_returns = []
# total_data = []
# trials = 1500
# for _ in range(trials):
#     profit, winning_trades,losing_trades,average_len,alpha = mac.moving_average_crossover_with_random_threshold(hist, cash, risk)
#     thereturn = (profit - cash) / cash
#     random_returns.append(thereturn)
#     total_data.append([thereturn, winning_trades, losing_trades, average_len,alpha])

# plt.hist(random_returns, bins=40, edgecolor='black')
# plt.xlabel('Return')
# plt.ylabel('Frequency')
# plt.title('Distribution of Returns with Random Thresholds')
# plt.grid(True)

# #sort total data by return and print
# total_data.sort(key=lambda x: x[0])

# for data in total_data:
#     print(f"Return: {data[0]:.2f}, Winning Trades: {data[1]}, Losing Trades: {data[2]}, Average Length: {data[3].days:.2f} days, Alpha: {data[4]:.4f}")

# plt.show()


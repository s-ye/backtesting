import numpy as np
import pandas as pd


stocks_monitor = ['NVDA']
strats_monitor = ['bollinger', 'avgdown', 'hf_crossover']

stocks_backtest = ['NVDA']
strats_backtest = ['bollinger', 'avgdown', 'hf_crossover']

risk = .02
cash = 10000
periods = [('3mo', '1h'), ('2y', '1h'), ('1y', '1d'), ('5y', '1d')]

def calculate_bollinger_bands(hist, period=20, std_dev=2):
    # Middle Band
    hist['Middle_Band'] = hist['Close'].rolling(window=period).mean()
    # Standard deviation of the close price
    hist['Std_Dev'] = hist['Close'].rolling(window=period).std()
    # Upper and Lower Bands
    hist['Upper_Band'] = hist['Middle_Band'] + (std_dev * hist['Std_Dev'])
    hist['Lower_Band'] = hist['Middle_Band'] - (std_dev * hist['Std_Dev'])

    # Drop the Std_Dev column if you don’t need it afterward
    hist.drop(columns=['Std_Dev'], inplace=True)


def calculate_macd(hist, fast_period=12, slow_period=26, signal_period=9):
    # Calculate the Fast and Slow EMAs
    hist['EMA_Fast'] = hist['Close'].ewm(span=fast_period, adjust=False).mean()
    hist['EMA_Slow'] = hist['Close'].ewm(span=slow_period, adjust=False).mean()
    # Calculate MACD line
    hist['MACD_Line'] = hist['EMA_Fast'] - hist['EMA_Slow']
    # Calculate Signal line
    hist['MACD_Signal'] = hist['MACD_Line'].ewm(span=signal_period, adjust=False).mean()
    # Optional: MACD Histogram (difference between MACD line and Signal line)
    hist['MACD_Histogram'] = hist['MACD_Line'] - hist['MACD_Signal']

    # Drop the EMA columns if you don’t need them afterward
    hist.drop(columns=['EMA_Fast', 'EMA_Slow'], inplace=True)


def processHist(hist):
    hist["Close"] = hist["Close"].astype(float)
    hist["Volume"] = hist["Volume"].astype(float)
    hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
    hist["SMA_200"] = hist["Close"].rolling(window=200).mean()
    hist["SMA_5"] = hist["Close"].rolling(window=5).mean()
    hist["SMA_10"] = hist["Close"].rolling(window=10).mean()
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

    # Boilinger Bands
    # MACD
    calculate_bollinger_bands(hist)
    calculate_macd(hist)

    
    # remove all the columns that are not numerical
    hist = hist.drop(columns=["Dividends", "Stock Splits"])
    # remove all the prices that are not close price
    hist = hist.drop(columns=["Open", "High", "Low"])

    return hist


import numpy as np

stocks = ['NVDA','NVO','CPNG', 'QCOM', 'INTC', 'UAL', 'SE', 'AMD', 'TSM', 'WW', 'VKTX']
strats = ['mac', 'rsi', 'avgdown']

stocks = ['UAL']
strats = ['avgdown']
risk = [.8]
addon = [.8]
relax = [10]
reevaluate = [10]
rsiparams = [(10000,x ,y) for x in risk for y in relax]
averagedownparams = [(10000,x,y,z) for x in risk for y in addon for z in reevaluate]
periods = [('3mo', '1h'), ('2y', '1h'), ('1y', '1d'), ('5y', '1d')]

def processHist(hist):
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
    
    return hist
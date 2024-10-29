from datetime import timedelta
import staticvariables as sv
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def trading_strategy_template(
    hist,
    buy_condition,
    sell_condition,
    addon_condition=None,
    cash=10000,
    risk=0.1,
    addon=0.01,
    reevaluate=5
):
    shares = 0
    previous_buy_price = 0
    previous_buy_date = hist.index[0]

    losing_trades = []
    winning_trades = []
    buy = []
    sell = []
    length_of_trades = []

    # DataFrames to store trade actions and closed positions
    trade_actions = pd.DataFrame(columns=["Date", "Action", "Amount", "Price"])
    closed_positions = pd.DataFrame(columns=["Buy Date", "Buy Price", "Sell Date", "Sell Price", "Profit", "Duration"])

    for i in range(15, len(hist)):
        # Check Buy Condition
        if buy_condition(hist, i):
            amount_to_invest = cash * risk
            shares += amount_to_invest / hist["Close"].iloc[i]
            cash -= amount_to_invest
            previous_buy_price = hist["Close"].iloc[i]
            previous_buy_date = hist.index[i]
            buy.append(i)

            # Record buy action
            new_action = pd.DataFrame([{"Date": hist.index[i], "Action": "Buy", "Amount": amount_to_invest, "Price": hist["Close"].iloc[i]}])
            new_action.dropna(axis=1, how='all', inplace=True)  # Remove all-NA columns
            new_action.dropna(how='all', inplace=True)          # Remove all-NA rows
            if not new_action.empty and new_action.shape[1] > 0:  # Ensure DataFrame is not empty and has columns
                trade_actions = pd.concat([trade_actions, new_action], ignore_index=True)

        # Check Sell Condition
        elif shares > 0 and sell_condition(hist, i):
            amount_to_sell = shares * hist["Close"].iloc[i]
            sell.append(i)
            cash += amount_to_sell
            profit = amount_to_sell - previous_buy_price * shares
            length = hist.index[i] - previous_buy_date

            # Record sell action
            new_action = pd.DataFrame([{"Date": hist.index[i], "Action": "Sell", "Amount": amount_to_sell, "Price": hist["Close"].iloc[i]}])
            new_action.dropna(axis=1, how='all', inplace=True)  # Remove all-NA columns
            new_action.dropna(how='all', inplace=True)          # Remove all-NA rows
            if not new_action.empty and new_action.shape[1] > 0:  # Ensure DataFrame is not empty and has columns
                trade_actions = pd.concat([trade_actions, new_action], ignore_index=True)

            # Record closed position
            new_position = pd.DataFrame([{
                "Buy Date": previous_buy_date,
                "Buy Price": previous_buy_price,
                "Sell Date": hist.index[i],
                "Sell Price": hist["Close"].iloc[i],
                "Profit": profit,
                "Duration": length
            }])
            new_position.dropna(axis=1, how='all', inplace=True)  # Remove all-NA columns
            new_position.dropna(how='all', inplace=True)          # Remove all-NA rows
            if not new_position.empty and new_position.shape[1] > 0:  # Ensure DataFrame is not empty and has columns
                closed_positions = pd.concat([closed_positions, new_position], ignore_index=True)

            if profit > 0:
                winning_trades.append(i)
            else:
                losing_trades.append(i)
            length_of_trades.append(length)
            shares = 0

        # Check Add-On Condition if available
        if addon_condition and i % reevaluate == 0 and len(buy) > 0 and shares > 0:
            if addon_condition(hist, i, previous_buy_price):
                amount_to_invest = cash * addon
                shares += amount_to_invest / hist["Close"].iloc[i]
                cash -= amount_to_invest
                previous_buy_price = hist["Close"].iloc[i]
                previous_buy_date = hist.index[i]
                buy.append(i)

                # Record add-on buy action
                new_action = pd.DataFrame([{"Date": hist.index[i], "Action": "Add-On Buy", "Amount": amount_to_invest, "Price": hist["Close"].iloc[i]}])
                new_action.dropna(axis=1, how='all', inplace=True)  # Remove all-NA columns
                new_action.dropna(how='all', inplace=True)          # Remove all-NA rows
                if not new_action.empty and new_action.shape[1] > 0:  # Ensure DataFrame is not empty and has columns
                    trade_actions = pd.concat([trade_actions, new_action], ignore_index=True)

    return cash + shares * hist["Close"].iloc[-1], winning_trades, losing_trades, length_of_trades, buy, sell, trade_actions, closed_positions


# A strategy is something which accepts a pandas datafram hist
# and returns a tuple of the form:
# (cash, winning_trades, losing_trades, length_of_trades, buy, sell)
# where cash is the amount of money the strategy has at the end of the backtest,
# winning_trades is the index of the trades that made money, losing_trades is the index of the trades that lost money,
# average_length_of_trades is the average length of the trades, buy is the index of the trades where the strategy bought,
# length_of_trades[i] is the length of the ith trade, 
# buy is the index of the trades where the strategy bought, and sell is the index of the trades where the strategy sold.
def applyStrategy(hist, strategy):
    if strategy == 'rsi':
        # RSI with moving average crossover strategy
        return trading_strategy_template(
            hist,
            buy_condition=lambda hist, i: ma_crossover_buy(hist, i) and hist["RSI"].iloc[i] < 30,
            sell_condition=ma_crossover_sell,
            cash=10000,
            risk=0.1,
            reevaluate=5
        )
    elif strategy == 'mac':
        # Moving Average Crossover without RSI condition
        return trading_strategy_template(
            hist,
            buy_condition=ma_crossover_buy,
            sell_condition=ma_crossover_sell,
            cash=10000,
            risk=0.1
        )
    elif strategy == 'avgdown':
        # Average down strategy with an add-on condition
        return trading_strategy_template(
            hist,
            buy_condition=ma_crossover_buy,
            sell_condition=ma_crossover_sell,
            addon_condition=rsi_addon_condition,
            cash=10000,
            risk=0.1,
            addon=0.01,
            reevaluate=5
        )
    elif strategy == 'bollinger':
        # Bollinger Bands strategy
        return trading_strategy_template(
            hist,
            buy_condition=bollinger_buy,
            sell_condition=bollinger_sell,
            cash=10000,
            risk=0.1
        )
    elif strategy == 'hf_crossover':
        # High-Frequency Moving Average Crossover (5- and 10-period MAs)
        return trading_strategy_template(
            hist,
            buy_condition=lambda hist, i: hist["SMA_5"].iloc[i] > hist["SMA_10"].iloc[i] and hist["RSI"].iloc[i] > 30 and hist["RSI"].iloc[i] < 70,
            sell_condition=lambda hist, i: hist["SMA_5"].iloc[i] < hist["SMA_10"].iloc[i] and hist["RSI"].iloc[i] > 30 and hist["RSI"].iloc[i] < 70,
            cash=10000,
            risk=0.1
        )


def ma_crossover_buy(hist, i):
    return hist["SMA_50"].iloc[i] > hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] < hist["SMA_200"].iloc[i-1]

def ma_crossover_sell(hist, i):
    return hist["SMA_50"].iloc[i] < hist["SMA_200"].iloc[i] and hist["SMA_50"].iloc[i-1] > hist["SMA_200"].iloc[i-1]

def bollinger_buy(hist, i):
    return hist["Close"].iloc[i] <= hist["Lower_Band"].iloc[i] and hist["RSI"].iloc[i] < 30

def bollinger_sell(hist, i):
    return hist["Close"].iloc[i] >= hist["Middle_Band"].iloc[i]

def rsi_addon_condition(hist, i, previous_buy_price):
    return hist["Close"].iloc[i] < previous_buy_price and hist["RSI"].iloc[i] < 30


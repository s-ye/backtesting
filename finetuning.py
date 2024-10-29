import strategies as s
import staticvariables as sv
import yfinance as yf


def write_header(file):
    file.write('Stock,Strategy,Period,Total,Winning Trades,Losing Trades,Length of Trades,Buy,Sell\n')

def process_stock(file, stock, period):
    hist = yf.Ticker(stock).history(period=period[0], interval=period[1])
    hist = sv.processHist(hist)
    if len(hist) == 0:
        return
    for strat in sv.strats_backtest:
        total, winning_trades, losing_trades, length_of_trades, buy, sell = s.applyStrategy(hist, strat)
        file.write(f'{stock},{strat},{period},{total},{winning_trades},{losing_trades},{length_of_trades},{buy},{sell}\n')

def main():
    with open('finetuning.txt', 'w') as f:
        write_header(f)
        for stock in sv.stocks_backtest:
            for period in sv.periods:
                process_stock(f, stock, period)

if __name__ == "__main__":
    main()

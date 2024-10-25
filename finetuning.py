import strategies as s
import staticvariables as sv
import yfinance as yf

def apply_strategy(hist, strat, rsiparams, averagedownparams):
    if strat == 'rsi':
        return s.rsifactor(hist, rsiparams, True)
    elif strat == 'mac':
        return s.rsifactor(hist, rsiparams, False)
    elif strat == 'avgdown':
        return s.averageDown(hist, averagedownparams)

def write_header(file):
    file.write('stock,strategy,rsiparams,averagedownparams,period,total,winning_trades,losing_trades,length_of_trades,buy,sell\n')

def process_stock(file, stock, period):
    hist = yf.Ticker(stock).history(period=period[0], interval=period[1])
    hist = sv.processHist(hist)
    if len(hist) == 0:
        return
    for strat in sv.strats:
        for rsiparams in sv.rsiparams:
            for averagedownparams in sv.averagedownparams:
                ss = strat + (str(rsiparams) if strat == 'rsi' else str(averagedownparams))
                total, winning_trades, losing_trades, length_of_trades, buy, sell = apply_strategy(hist, strat, rsiparams, averagedownparams)
                file.write(f'{stock},{ss},{period},{total},{winning_trades},{losing_trades},{length_of_trades},{buy},{sell}\n')

def main():
    with open('finetuning.txt', 'w') as f:
        write_header(f)
        for stock in sv.stocks:
            for period in sv.periods:
                process_stock(f, stock, period)

if __name__ == "__main__":
    main()

from datetime import datetime
import backtrader as bt
import pandas as pd


# Create a subclass of Strategy to define the indicators and logic
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=50,  # period for the fast moving average
        pslow=200   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.order_target_size(target=1)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.order_target_size(target=0)  # close long position


def getData(datapath):
    dataframe = pd.read_csv(datapath, parse_dates=True, index_col=0)

    print('--------------------------------------------------')
    print(dataframe)
    print('--------------------------------------------------')

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)
    return data


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

datapath = '/home/alex/PycharmProjects/ML4AT/data/backtrader/datas/2006-01-02-volume-min-001.txt'
data = getData(datapath)
cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command

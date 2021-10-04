import datetime  # For datetime objects
import os
import sys  # To find out the script name (in argv[0])
import pandas as pd
from os.path import join

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        # self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.tokens = [i._name for i in self.datas]

        # Add a MovingAverageSimple indicator
        self.sma = {}
        for i, token in enumerate(self.tokens):
            self.sma[token] = bt.indicators.SimpleMovingAverage(
                self.datas[i], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        for i, token in enumerate(self.tokens):
            close_px = self.datas[i].close[0]
            sma_px = self.sma[token][0]

            # Simply log the closing price of the series from the reference
            self.log('Token:{}|Close:{}|SMA:{}'.format(token, close_px, sma_px))
            #
            # # Check if an order is pending ... if yes, we cannot send a 2nd one
            if self.order:
                # return
                pass

            # # Check if we are in the market
            if not self.positionsbyname[token]:

                # Not yet ... we MIGHT BUY if ...
                if close_px > sma_px:

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %s %.2f' % (token, close_px))

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

            else:

                if close_px < sma_px:
                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()

                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log('SELL CREATE, %s %.2f' % (token, close_px))


if __name__ == '__main__':
    DATA_DIR = "/home/alex/PycharmProjects/machine-learning-for-trading/data/crypto/Token Data/Bitfinex"
    TOKENS = ['BTCUSD','ETHUSD','BALUSD']
    FREQ = '1d'
    CASH = 100000

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Order sizing
    cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    # Add data
    for token in TOKENS:
        df = pd.read_pickle(join(DATA_DIR, '{}_{}_2020-01-01 00:00:00.pkl'.format(token, FREQ)))
        df.drop(columns=['averageOHLC'], inplace=True)
        df['OI'] = 0
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data, name=token)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')

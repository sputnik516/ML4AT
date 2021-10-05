from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
from os.path import join

import pandas as pd

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.utils.flushfile
from weekdaysfiller import WeekDaysFiller


class St(bt.Strategy):
    params = (('sma', 0),)

    def __init__(self):
        if self.p.sma:
            btind.SMA(self.data0, period=self.p.sma)
            btind.SMA(self.data1, period=self.p.sma)

    def next(self):
        dtequal = (self.data0.datetime.datetime() ==
                   self.data1.datetime.datetime())

        txt = ''
        txt += '%04d, %5s' % (len(self), str(dtequal))
        txt += ', data0, %s' % self.data0.datetime.datetime().isoformat()
        txt += ', %s, data1' % self.data1.datetime.datetime().isoformat()
        print(txt)


def runstrat():
    args = parse_args()

    # fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
    # todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
    fromdate = datetime.datetime(year=2020,month=1,day=1)
    todate = datetime.datetime(year=2021,month=9,day=4)

    cerebro = bt.Cerebro(stdstats=False)

    # DataFeed = btfeeds.YahooFinanceCSVData
    # if args.online:
    #     DataFeed = btfeeds.YahooFinanceData
    #
    # data0 = DataFeed(dataname=args.data0, fromdate=fromdate, todate=todate)
    DATA_DIR = "/home/alex/PycharmProjects/ML4AT/data/crypto/Token Data/Bitfinex"
    TOKENS = ['BTCUSD', 'ETHUSD', 'BALUSD']
    FREQ = '1d'
    data0 = bt.feeds.PandasData(dataname=pd.read_pickle(join(DATA_DIR, '{}_{}_2020-01-01 00:00:00.pkl'.format(TOKENS[0], FREQ))))

    if args.data1:
        # data1 = DataFeed(dataname=args.data1, fromdate=fromdate, todate=todate)
        data1 = bt.feeds.PandasData(dataname=pd.read_pickle(join(DATA_DIR, '{}_{}_2020-01-01 00:00:00.pkl'.format(TOKENS[2], FREQ))))
    else:
        data1 = data0.clone()

    if args.filler or args.filler0:
        data0.addfilter(WeekDaysFiller, fillclose=args.fillclose)

    if args.filler or args.filler1:
        data1.addfilter(WeekDaysFiller, fillclose=args.fillclose)

    cerebro.adddata(data0)
    cerebro.adddata(data1)

    cerebro.addstrategy(St, sma=args.sma)
    cerebro.run(runonce=True, preload=True)

    if args.plot:
        cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for aligning with trade ')

    parser.add_argument('--online', required=False, action='store_true',
                        help='Fetch data online from Yahoo')

    parser.add_argument('--data0', required=True, help='Data 0 to be read in')
    parser.add_argument('--data1', required=False, help='Data 1 to be read in')

    parser.add_argument('--sma', required=False, default=0, type=int,
                        help='Add a sma to the datas')

    parser.add_argument('--fillclose', required=False, action='store_true',
                        help='Fill with Close price instead of NaN')

    parser.add_argument('--filler', required=False, action='store_true',
                        help='Add Filler to Datas 0 and 1')

    parser.add_argument('--filler0', required=False, action='store_true',
                        help='Add Filler to Data 0')

    parser.add_argument('--filler1', required=False, action='store_true',
                        help='Add Filler to Data 1')

    parser.add_argument('--fromdate', '-f', default='2012-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t', default='2012-12-31',
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--plot', required=False, action='store_true',
                        help='Do plot')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
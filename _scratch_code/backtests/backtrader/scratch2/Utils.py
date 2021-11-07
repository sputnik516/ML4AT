import backtrader as bt
import pandas as pd
from os.path import join


DEFAULT_FDIR = "/home/alex/PycharmProjects/ML4AT/data/backtrader/datas"


def getDataPandasCSV(fName, fDir=DEFAULT_FDIR):
    fPth = join(fDir, fName)
    dataframe = pd.read_csv(fPth, parse_dates=True, index_col=0)

    print('--------------------------------------------------')
    print('Data source: {}'.format(fPth))
    print(dataframe)
    print('--------------------------------------------------')

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)
    return data

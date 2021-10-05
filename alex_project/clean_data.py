import pandas as pd
from datetime import datetime as dt
from os.path import join


DATA_DIR = "/home/alex/PycharmProjects/ML4AT/data/crypto/Token Data/Bitfinex"
TOKENS = ['BTCUSD', 'ETHUSD', 'BALUSD']
FREQ = '1d'

start = dt(year=2020, month=1, day=1)
end = dt(year=2021, month=9, day=4)
dt_rng = pd.date_range(start=start, end=end, freq=FREQ)

data = pd.DataFrame(index=dt_rng)

for token in TOKENS:
    df = pd.read_pickle(join(DATA_DIR, '{}_{}_2020-01-01 00:00:00.pkl'.format(token, FREQ)))
    df.columns = ['{}_{}'.format(token, col) for col in df.columns]
    data = data.merge(right=df, how='left', left_index=True, right_index=True)

data.to_pickle(join(DATA_DIR, 'combined_data_{}_01012020-09042021.pkl'.format(FREQ)))

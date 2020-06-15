from pandas import DataFrame
import numpy as np
from pathlib import Path
import re
from pandas import DataFrame, read_json, to_datetime


DEFAULT_DATAFRAME_COLUMNS = [
    'date',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'closeTime',
    'quoteVolume',
    'pchange1h',
    'pchange1hpct',
    'pchange24h',
    'pchange24hpct',
    'v1h',
    'vchange1h',
    'vchange1hpct',
    'v4h',
    'vchange4h',
    'vchange4hpct',
    'v24',
    'vchange24h',
    'vchange24hpct']


class Store:

    _columns = DEFAULT_DATAFRAME_COLUMNS
    _dataFolder = 'user_data/data'

    def __init__(self):
        import os
        if not os.path.isdir(self._dataFolder):
            os.mkdir(self._dataFolder)

    def store_data(self,
                   pair: str,
                   timeframe: str,
                   data: DataFrame):

        filename = f"{self._dataFolder}/{pair.replace('/', '_')}_{timeframe}"
        _data = data.copy()
        # Convert date to int
        _data['date'] = _data['date'].astype(np.int64) // 1000 // 1000

        # Reset index, select only appropriate columns and save as json
        _data = _data.reset_index(drop=True).loc[:, self._columns]
        _data.to_json(f"{filename}.json", orient="values")
        _data.to_csv(f"{filename}.csv", mode='a', header=True)

    def load_data(self, pair: str, timeframe: str) -> DataFrame:
        """
        Internal method used to load data for one pair from disk.
        Implements the loading and conversion to a Pandas dataframe.
        Timerange trimming and dataframe validation happens outside of this method.
        :param pair: Pair to load data
        :param timeframe: Timeframe (e.g. "5m")
        :param timerange: Limit data to be loaded to this timerange.
                        Optionally implemented by subclasses to avoid loading
                        all data where possible.
        :return: DataFrame with ohlcv data,
 or empty DataFrame
        """
        filename = f"{self._dataFolder}/{pair.replace('/', '_')}_{timeframe}.json"
        if not filename.exists():
            return DataFrame(columns=self._columns)
        pairdata = read_json(filename, orient='values')
        pairdata.columns = self._columns
        pairdata = pairdata.astype(dtype={'open': 'float',
                                          'high': 'float',
                                          'low': 'float',
                                          'close': 'float',
                                          'volume': 'float',
                                          'quoteVolume': 'float',
                                          'pchange1h': 'float',
                                          'pchange1hpct': 'float',
                                          'pchange24h': 'float',
                                          'pchange24hpct': 'float',
                                          'v1h': 'float',
                                          'vchange1h': 'float',
                                          'vchange1hpct': 'float',
                                          'v4h': 'float',
                                          'vchange4h': 'float',
                                          'vchange4hpct': 'float',
                                          'v24': 'float',
                                          'vchange24h': 'float',
                                          'vchange24hpct': 'float'})
        pairdata['date'] = to_datetime(pairdata['date'], unit='ms',
                                       utc=True, infer_datetime_format=True)
        return pairdata

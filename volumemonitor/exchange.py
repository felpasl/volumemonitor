import ccxt
import pandas as pd
from pandas import DataFrame, to_datetime
from binance.client import Client 
import arrow

class Exchange:

    exchange: ccxt.Exchange
    binance: Client

    def __init__(self, config):
        exchange_class = getattr(ccxt, config['exchange']['name'])
        self.exchange = exchange_class(config['exchange'])

        self.binance = Client(config['exchange']['key'], config['exchange']['secret'])
        

    def ValidatePairs(self, pairs):
        
        markets = self.exchange.load_markets()

        for pair in pairs:
            if pair not in markets:
                raise Exception(f'The Exchange does not contain this Pair: {pair}')

    def fetchOHLCV(self, pair, timeframe: str, start: str) -> DataFrame:      

        data = self.binance.get_historical_klines(pair.replace('/', ''), timeframe, start)
        return pd.DataFrame(data)

def timeframe_to_minutes(timeframe: str) -> int:
    """
    Same as timeframe_to_seconds, but returns minutes.
    """
    return ccxt.Exchange.parse_timeframe(timeframe) // 60

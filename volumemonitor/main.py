import json
from readConfig import readConfig
from exchange import Exchange
from volumeGainer import calculate_gainer
from store import Store
timeframe = '1h'
size = 50

def Main():
    config = readConfig()
    exchange = Exchange(config)

    pairs = config['exchange']['pair_list']
    exchange.ValidatePairs(pairs)

    store = Store()
    for pair in pairs:
        print(f"Get {pair} {timeframe}")
        df = exchange.fetchOHLCV(pair, timeframe, f"{size} hours ago")
        if not df.empty:
            df = calculate_gainer(df)
            store.store_data(pair=pair,timeframe=timeframe,data=df)
            print(f"Returned {pair} {df.size} lines")
        else:
            print(f"Returned {pair} Empty!")
Main()
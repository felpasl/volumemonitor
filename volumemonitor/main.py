import json
from readConfig import readConfig
from exchange import Exchange
from volumeGainer import calculate_gainer
from store import Store
from telegramMonitor import Telegram
import time 
timeframe = '1h'
size = 50

def Main():
    config = readConfig()
    exchange = Exchange(config)

    pairs = config['exchange']['pair_list']
    exchange.ValidatePairs(pairs)

    store = Store()

    telegram = Telegram(config)

    while True:
        for pair in pairs:
            print(f"Get {pair} {timeframe}")
            df = exchange.fetchOHLCV(pair, timeframe, f"{size} hours ago")
            if not df.empty:
                df_old = store.load_data(pair,timeframe)
                df = calculate_gainer(df)
                if not df_old.empty:
                    df_old.append(df)
                else:
                    df_old = df
                store.store_data(pair=pair,timeframe=timeframe,data=df_old)
                print(f"Returned {pair} {df.size} lines")
            else:
                print(f"Returned {pair} Empty!")    
Main()
from pandas import DataFrame
import pandas as pd 


def calculate_gainer(df: DataFrame) -> DataFrame:
    
    if not df.empty:
        df.columns = ['date','open','high','low','close','volume','closeTime','quoteVolume','numberTrades','TakerBuyBaseVolume','TakerBuyQuoteVolume','x']
       
        del df['x']

        df ["open"] = pd.to_numeric(df["open"])
        df ["high"] = pd.to_numeric(df["high"])
        df ["low"] = pd.to_numeric(df["low"])
        df ["close"] = pd.to_numeric(df["close"])
        df ["volume"] = round(pd.to_numeric(df["volume"]))
        df ["quoteVolume"] = round(pd.to_numeric(df["quoteVolume"]))
        # df.loc[df.quoteVolume < 100, 'quoteVolume'] = 100

        df['pchange1h'] = pd.to_numeric(df['close']).diff(1).fillna(0) # diff can has if for different timeperiods 
        df['pchange1hpct'] = round((pd.to_numeric(df['pchange1h'])/df ["close"])*100,2)

        df['pchange24h'] = df.close.diff(23).fillna(0) # diff can has if for different timeperiods 
        df['pchange24hpct'] = round((df['pchange24h']/df ["close"])*100,2)

        df['v1h'] = df.quoteVolume.rolling(window = 1).sum().fillna(0)#.shift()

        df['vchange1h'] = df.v1h.diff(1).fillna(0) # diff can has if for different timeperiods 
        df['vchange1hpct'] = round((df['vchange1h']/df ["quoteVolume"])*100,2)
    
        df['v4h'] = df.quoteVolume.rolling(window = 4).sum().fillna(0)#.shift()
        df['vchange4h'] = df.v4h.diff(4).fillna(0) # diff can has if for different timeperiods 
        df['vchange4hpct'] = round((df['vchange4h']/df ["v4h"])*100,2)
        
        df['v24'] = df.quoteVolume.rolling(window = 23).sum().fillna(0)#.shift()
        df['vchange24h'] = df.v24.diff(23).fillna(0) # diff can has if for different timeperiods 
        df['vchange24hpct'] = round((df['vchange24h']/df ["v24"])*100,2).fillna(0)

    return df
import requests
import pandas as pd
import time
import webbrowser

chosen_time = '15' #1,3,5,10,15,30,60,120,240 분 단위
chosen_coin = 'ETH' # 비트코인, 이더리움, 등등
coin = 'KRW-' + chosen_coin

url = "https://api.upbit.com/v1/candles/minutes/{}".format(chosen_time)

querystring = {"market":"KRW-BTC","count":"500"}
querystring['market'] = coin

response = requests.request("GET", url, params=querystring)

data = response.json()

df = pd.DataFrame(data)

df=df.reindex(index=df.index[::-1]).reset_index()

df['close']=df["trade_price"]

def rsi(ohlc: pd.DataFrame, period: int = 14):
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    rsi = pd.Series(100 - (100 / (1 + RS)), name="RSI")
    rsi = rsi(df, 14).iloc[-1]
    return('Upbit {} minute {} RSI:{}'.format(chosen_time, chosen_coin, rsi))


# def rsi(ohlc: pd.DataFrame, period: int = 14):
#     ohlc["close"] = ohlc["close"]
#     delta = ohlc["close"].diff()

#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0

#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# rsi = rsi(df, 14).iloc[-1]

# return('Upbit {} minute {} RSI:{}'.format(chosen_time, chosen_coin, rsi))



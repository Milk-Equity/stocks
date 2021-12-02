import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import time
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

api_key = '7DOY154L31ZDC2PG'


def stocks(ticker):
    ticker = ticker.upper()
    ts = TimeSeries(key='7DOY154L31ZDC2PG', output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
    df = pd.DataFrame(data)
    # df = df.reset_index(level=0)
    df = df.rename(columns={"4. close": "Close",
                            "7. dividend amount": "Dividend",
                            "2. high": "High",
                            "3. low": "Low",
                            "1. open": "Open",
                            "8. split coefficient": "Split Coefficient",
                            "6. volume": "Volume"})
    df = df.drop('5. adjusted close', 1)

    new = df.sort_index(ascending=False)

    split_coef = new['Split Coefficient'].shift(1
                                                ).fillna(1).cumprod()

    for col in ['Open', 'High', 'Low', 'Close']:
        new['Adj.' + col] = new[col] / split_coef
    new['Adj.Volume'] = split_coef * new['Volume']
    dividends = False
    if dividends:
        new['Adj. Dividends'] = new['Dividend Amount'] / split_coef
    new['Daily Change'] = new['Adj.Close'] - new['Adj.Open']
    new['30Day'] = new['Adj.Close'].rolling(window=30, min_periods=1).mean()
    new['60Day'] = new['Adj.Close'].rolling(window=60, min_periods=1).mean()
    new = new.last('2Y')
    return new.sort_index(ascending=True)

apple = stocks('aapl')

#CandleStick
def candlestick(ticker, name):
    c_candlestick = go.Figure(data = [go.Candlestick(x = ticker.index,
                                               open = ticker[('Adj.Open')],
                                               high = ticker[('Adj.High')],
                                               low = ticker[('Adj.Low')],
                                               close = ticker[('Adj.Close')])])

    c_candlestick.update_xaxes(
        title_text = 'Date',
        rangeslider_visible = True,
        rangeselector = dict(
            buttons = list([
                dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')])))

    c_candlestick.update_layout(
        title = {
            'text': '%s Share Price (Life Time)' % (name),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    c_candlestick.update_yaxes(title_text = 'Price', tickprefix = '$')
    return c_candlestick.show()

st.title('Test')


st.plotly_chart(candlestick(apple, 'Apple'), use_container_width=True)

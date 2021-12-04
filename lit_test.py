import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import MACD
from ta.momentum import StochasticOscillator # MACD
import streamlit as st

ticker = st.sidebar.text_input('Symbol', value='AAPl', max_chars=5)

df = yf.download(ticker, auto_adjust=True, period = '3Y')

fig = go.Figure()
# add OHLC trace
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             showlegend=False))








st.plotly_chart(fig, use_container_width=True)


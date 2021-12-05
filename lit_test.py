import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import MACD
from ta.momentum import StochasticOscillator # MACD
import streamlit as st
from datetime import datetime as dt
import datetime

#Get Ticker
ticker = st.sidebar.text_input('Symbol', value='AAPl', max_chars=4)

#Get Date
#today = datetime.datetime.strptime(date, "%m/%d/%Y")
#today = datetime.date.today()
date = datetime.date.today()
d = st.sidebar.date_input("Starting Date", datetime.date(2019, 7, 6), max_value=date)


#Download data from Date and Ticker
df = yf.download(ticker, auto_adjust=True, start=d)
                 #period = '3Y')



# removing all empty dates
# build complete timeline from start date to end date
dt_all = pd.date_range(start=df.index[0],end=df.index[-1])

# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]

# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]


fig = go.Figure()
# add OHLC trace
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             showlegend=False))
fig.update_layout(title=ticker)







st.plotly_chart(fig, use_container_width=False)


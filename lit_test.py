import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import MACD
from ta.momentum import StochasticOscillator # MACD
import streamlit as st
import datetime
import numpy as np
import yahoo_fin.stock_info as si
import plotly.figure_factory as ff

#Page Config
st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
#Get Ticker
ticker = st.sidebar.text_input('Symbol', value='AAPl', max_chars=4)

#Get Date
date = datetime.date.today()
#Sidebar
d = st.sidebar.date_input("Starting Date", datetime.date(2012, 1, 6), max_value=date)


#Download data from Date and Ticker
df = yf.download(ticker, auto_adjust=True, start=d, period = '1Y')


#Data Cleaning DON'T DELETE
#removing all empty dates
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
#fig.update_layout(title=ticker)

#Fundamentals
fund = si.get_quote_table(ticker, dict_result=False)
fund.columns = ['Fundamentals ', 'Data']
fig_fund =  ff.create_table(fund)



#Starting Layout
col1, col2 = st.columns([1, 3])


with col1:
    col1.subheader("Stock Fundamentals")
    st.plotly_chart(fig_fund, use_container_width=True)

with col2:
    st.subheader(ticker)
    st.plotly_chart(fig, use_container_width=True)
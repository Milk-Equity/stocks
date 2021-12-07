import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import MACD
from ta.momentum import StochasticOscillator  # MACD
import streamlit as st
import datetime
import yahoo_fin.stock_info as si
import plotly.figure_factory as ff
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Milk Equity",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Get Ticker
ticker = st.sidebar.text_input('Symbol', value='AAPL', max_chars=4)
ticker = ticker.upper()
# Get Date
date = datetime.date.today()

# Sidebar
d = st.sidebar.date_input("Starting Date", datetime.date(2012, 1, 6), max_value=date)
ytd = st.sidebar.button('YTD')

# Download data from Date and Ticker
df = yf.download(ticker, auto_adjust=True, start=d, period='1Y')

# Data Cleaning DON'T DELETE
# removing all empty dates
# build complete timeline from start date to end date
dt_all = pd.date_range(start=df.index[0], end=df.index[-1])

# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]

# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

# MACD
df['MA60'] = df['Close'].rolling(window=60).mean()
df['MA30'] = df['Close'].rolling(window=30).mean()

# Daily Change
df['Daily Change'] = df['Close'] - df['Open']


#Colors for chart... doesn't work
def colors(df):
    dc = df['Daily Change'].iloc[-1]
    if dc < 0:
        return 'green'
    else:
        return 'red'


fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', fill='tozeroy', line={'color': colors(df)}))

# Fundamentals
fund = si.get_quote_table(ticker, dict_result=False)
fund.columns = ['Fundamentals ', 'Data']
fig_fund = ff.create_table(fund)

# Starting Layout
col1, col2 = st.columns([1, 3])

with col1:
    col1.subheader("Stock Fundamentals")
    st.plotly_chart(fig_fund, use_container_width=True)

with col2:
    st.subheader(ticker)
    st.plotly_chart(fig, use_container_width=True)

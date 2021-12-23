import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta

import yahoo_fin.stock_info as si
import plotly.figure_factory as ff

# Page Config
st.set_page_config(
    page_title="Milk Equity",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Get Ticker
symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=4)
symbol = symbol.upper()

# Get Date
todays_date = datetime.date.today()
one_day = datetime.date.today() - relativedelta(days=1)
five_days = datetime.date.today() - relativedelta(days=5)
one_month = datetime.date.today() - relativedelta(months=1)
three_months = datetime.date.today() - relativedelta(months=3)
six_months = datetime.date.today() - relativedelta(months=6)
yr_ago = datetime.date.today() - relativedelta(years=1)
two_yrs_ago = datetime.date.today() - relativedelta(years=2)
three_yrs_ago = datetime.date.today() - relativedelta(years=3)
five_yrs_ago = datetime.date.today() - relativedelta(years=5)

# Download data from Date and Ticker
@st.cache
def get_data(symbol):
    df = yf.download(symbol, auto_adjust=True)
    df['Daily Change'] = df['Close'] - df['Open']
    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])

    # retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]

    # define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    return df
df = get_data(symbol)

def colors(df):
    oldest = df['Close'].iloc[0] #0 is first -1 is last
    today = df['Close'].iloc[-1]
    color_num = today - oldest
    if color_num > 0:
        return 'green'
    else:
        return 'red'

#Main Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.Date, y=df.Close, mode='lines', fill='tozeroy', line={'color': colors(df)}))

# Fundamentals
@st.cache
def fundamentals(symbol):
    fund = si.get_quote_table(symbol, dict_result=False)
    fund.columns = ['Fundamentals ', 'Data']
    fig_fund = ff.create_table(fund)
    return fig_fund



# Starting Layout
col1, col2 = st.columns([1,4])

with col1:
    col1.subheader("Stock Fundamentals")
    st.plotly_chart(fundamentals(symbol), use_container_width=True)

with col2:
    st.subheader(symbol)
    date_options = ['1D','5D','1M','3M','6M','1YR','2YR','3YR','5Yrs','MAX']
    date = st.select_slider('Graph Range',options = date_options, value = '1M')
    if date == '1D':
        df = df.loc[one_day:todays_date]
    if date == '5D':
        df = df.loc[five_days:todays_date]
    if date == '1M':
        df = df.loc[one_month:todays_date]
    if date == '3M':
        df = df.loc[three_months:todays_date]
    if date == '6M':
        df = df.loc[six_months:todays_date]
    if date == '1YR':
        df = df.loc[yr_ago:todays_date]
    if date == '2YR':
        df = df.loc[two_yrs_ago:todays_date]
    if date == '3YR':
        df = df.loc[three_yrs_ago:todays_date]
    if date == '5Yrs':
        df = df.loc[five_yrs_ago:todays_date]
    if date == 'MAX':
        df = df
    # Main Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', fill='tozeroy', line={'color': colors(df)}))
    st.plotly_chart(fig, use_container_width=True)
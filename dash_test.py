import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#from ta.trend import MACD
#from ta.momentum import StochasticOscillator  # MACD
import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta

import yahoo_fin.stock_info as si
import plotly.figure_factory as ff
#import plotly.express as px



# Get Ticker
symbol = st.sidebar.text_input('Symbol', value='MSFT', max_chars=4)
symbol = symbol.upper()
# Get Date
todays_date = datetime.date.today()
yr_ago = datetime.date.today() - relativedelta(years=1)
two_yrs_ago = datetime.date.today() - relativedelta(years=2)
three_yrs_ago = datetime.date.today() - relativedelta(years=3)

# Sidebar

date = st.sidebar.date_input("Starting Date", datetime.date(2019,1,5), max_value=todays_date)
ytd = st.sidebar.button('YTD')



# todo date picker doesn't work





@st.cache
def get_data(symbol):
    df = yf.download(symbol, auto_adjust=True)
    df['Daily Change'] = df['Close'] - df['Open']
    return df
df = get_data(symbol)


if st.sidebar.button('1 Year'):
    df = df.loc[yr_ago:todays_date]
if st.sidebar.button('2 Years'):
    df = df.loc[two_yrs_ago:todays_date]

#df = df.loc[three_yrs_ago:todays_date]




# build complete timeline from start date to end date
dt_all = pd.date_range(start=df.index[0], end=df.index[-1])

# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]

# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]





#Colors for chart
def colors(df):
    dc = df['Daily Change'].iloc[-1]
    if dc > 0:
        return 'green'
    else:
        return 'red'


#Main Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', fill='tozeroy', line={'color': colors(df)}))

# Fundamentals
fund = si.get_quote_table(symbol, dict_result=False)
fund.columns = ['Fundamentals ', 'Data']
fig_fund = ff.create_table(fund)

# Starting Layout
st.plotly_chart(fig, use_container_width=True)
st.write(three_yrs_ago)
st.write(three_yrs_ago.strftime('%Y/%M/%D'))
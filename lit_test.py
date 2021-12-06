import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import MACD
from ta.momentum import StochasticOscillator # MACD
import streamlit as st
import datetime
import yahoo_fin.stock_info as si
import plotly.figure_factory as ff
import plotly.express as px


#Page Config
st.set_page_config(
    page_title="Milk Equity",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
#Get Ticker
ticker = st.sidebar.text_input('Symbol', value='AAPL', max_chars=4)
ticker = ticker.upper()
#Get Date
date = datetime.date.today()
#Sidebar
d = st.sidebar.date_input("Starting Date", datetime.date(2012, 1, 6), max_value=date)


#Download data from Date and Ticker
df = yf.download(ticker, auto_adjust=True, start=d)
                 #, period = '1Y')


#Data Cleaning DON'T DELETE
#removing all empty dates
# build complete timeline from start date to end date
dt_all = pd.date_range(start=df.index[0],end=df.index[-1])

# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]

# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

#MACD
df['MA60'] = df['Close'].rolling(window=60).mean()
df['MA30'] = df['Close'].rolling(window=30).mean()

#Daily Change
df['Daily Change'] = df['Close'] - df['Open']

# first declare an empty figure
fig = make_subplots(rows=2, row_heights=[0.5,0.1])

# add Candlestick trace
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             showlegend=False))
# add moving average traces
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA30'],
                         line=dict(color='blue', width=2),
                         name='MA 30'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA60'],
                         line=dict(color='orange', width=2),
                         name='MA 60'))

# Plot volume trace on 2nd row
colors = ['green' if row['Open'] - row['Close'] >= 0
          else 'red' for index, row in df.iterrows()]
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     marker_color=colors
                    ), row=2, col=1)
#Layout stuff
fig.update_layout(height=900, width=1200,
                  showlegend=False,
                  xaxis_rangeslider_visible=False,)
                  #xaxis_rangebreaks=[dict(values=dt_breaks)])

#Update y-axis label
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

#Fundamentals
fund = si.get_quote_table(ticker, dict_result=False)
fund.columns = ['Fundamentals ', 'Data']
fig_fund =  ff.create_table(fund)

area_chart = px.line(df['Daily Change'])

# Create subplots and mention plot grid size
fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,
               vertical_spacing=0.03, subplot_titles=('Price', 'Volume'),
               row_width=[0.2, 0.7])

# Plot OHLC on 1st row
fig1.add_trace(px.line(dfrow=1, col=1)

# Bar trace for volumes on 2nd row without legend
fig1.add_trace(go.Bar(x=df.index, y=df['Volume'], showlegend=False), row=2, col=1)

# Do not show OHLC's rangeslider plot
fig1.update(layout_xaxis_rangeslider_visible=False)

#Starting Layout
col1, col2 = st.columns([1, 3])


with col1:
    col1.subheader("Stock Fundamentals")
    st.plotly_chart(fig_fund, use_container_width=True)

with col2:
    st.subheader(ticker)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(area_chart)
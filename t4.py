import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

import streamlit as st

st.set_page_config(layout="wide")

symbol = st.sidebar.text_input('Symbol', value='MSFT', max_chars=4)
symbol = symbol.upper()


df = yf.download(symbol, auto_adjust=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', fill='tozeroy'))

col1, col2 = st.columns([1,4])

with col1:
    col1.subheader("Please work")
    date_options = ['1D','5D','10D']
    date = st.select_slider('Chose a Date', options = date_options)
with col2:
    st.plotly_chart(fig, use_container_width=True)


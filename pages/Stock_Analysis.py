import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from pages.utils import plotly_figure
import numpy as np
npNaN = np.nan
st.set_page_config(page_title="Stock Analysis", 
                layout="wide",
                page_icon="page_with_curl",
                )


st.title("Stock Analysis")
st.header("Analyze Stock Data with Technical Indicators")

col1, col2, col3 = st.columns(3)

today = datetime.datetime.today()

with col1: 
    ticker = st.text_input("Stock Name","TSLA")

with col2:
    start_date = st.date_input("Choose Start Date",datetime.date(today.year-1,today.month,today.day))

with col3:
    end_date = st.date_input("Choose End Date",datetime.date(today.year-1,today.month,today.day))


st.subheader(ticker)

stock = yf.Ticker(ticker)

summary = stock.info.get("longBusinessSummary", "No summary available.") 
st.write(summary)

sector = stock.info.get("sector")
st.write("**Sector:**", sector)

emp = stock.info.get('fullTimeEmployees')
st.write("**Full Time Employee:**",emp)

web = stock.info.get('website')
st.write("**Website:**",web)

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['Maket Cap','Beta','EPS','PE Ratio'])
    df[''] = [stock.info.get('marketCap',npNaN), stock.info.get('beta',npNaN), stock.info.get('trailingEps',npNaN), stock.info.get('trailingPE',npNaN)]
    fig_plot = plotly_figure.plotly_table(df)
    st.plotly_chart(fig_plot, use_container_width=True)

with col2:
    df2 = pd.DataFrame(index=['Quick Ratio','Revenue per Share','Profit Margins','Dept to Equity','Return on Equity'])
    df2[''] = [stock.info.get('quickRatio',npNaN), stock.info.get('revenuePerShare',npNaN), stock.info.get('profitMargins',npNaN), stock.info.get('debtToEquity',npNaN),stock.info.get('returnOnEquity',npNaN)]
    fig_plot2 = plotly_figure.plotly_table(df2)
    st.plotly_chart(fig_plot2, use_container_width=True)

data = yf.download(ticker, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)
if not data.empty and 'Close' in data.columns:
    if len(data) >= 2:
        daily_change = float(data['Close'].iloc[-1]) - float(data['Close'].iloc[-2])
        col1.metric("Closing Price", f"{float(data['Close'].iloc[-1]):.2f}", f"{daily_change:.2f}")
    elif len(data) == 1:
        #col1.metric("Closing Price", f"{data['Close'].iloc[-1]:.2f}", "N/A")
        closing_price = float(data['Close'].iloc[-1])
        col1.metric("Closing Price", f"{closing_price:.2f}", "N/A")
    else:
        col1.metric("Closing Price", "N/A", "N/A")
else:
    col1.metric("Closing Price", "N/A", "N/A")


last_10_df = data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_figure.plotly_table(last_10_df)

st.write("### Last 10 Days Stock Data")
st.plotly_chart(fig_df, use_container_width=True)

cols = st.columns(12)

num_period = ''

with cols[1]:
    if st.button('5D'):
        num_period = '5D'
with cols[2]:
    if st.button('1M'):
        num_period = '1M'
with cols[3]:
    if st.button('6M'):
        num_period = '6M'
with cols[4]:
    if st.button('YTD'):
        num_period = 'YTD'
with cols[5]:
    if st.button('1Y'):
        num_period = '1Y'
with cols[6]:
    if st.button('5Y'):
        num_period = '5Y'
with cols[7]:
    if st.button('Max'):
        num_period = 'Max'

col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox("", ["Candle","Line"])
with col2:
    if chart_type == "Candle":
        indicator = st.selectbox("", ["RSI","MACD"])
    else:
        indicator = st.selectbox("", ["RSI","Moving Average","MACD"])


ticker = yf.Ticker(ticker)
new_df1 = ticker.history(period='max')
data1 = ticker.history(period='max')
if num_period == '':
    if chart_type == "Candle" and indicator == "RSI":
        st.plotly_chart(plotly_figure.candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(plotly_figure.RSI(data1, '1y'), use_container_width=True)
    
    if chart_type == "Candle" and indicator == "MACD":
        st.plotly_chart(plotly_figure.candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(plotly_figure.MACD(data1, '1y'), use_container_width=True)
    
    if chart_type == "Line" and indicator == "RSI":
        st.plotly_chart(plotly_figure.close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(plotly_figure.RSI(data1, '1y'), use_container_width=True)
    
    if chart_type == "Line" and indicator == "Moving Average":
        st.plotly_chart(plotly_figure.Moving_average(data1, '1y'), use_container_width=True)
    
    if chart_type == "Line" and indicator == "MACD":
        st.plotly_chart(plotly_figure.close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(plotly_figure.MACD(data1, '1y'), use_container_width=True)
else:
    if chart_type == "Candle" and indicator == "RSI":
        st.plotly_chart(plotly_figure.candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(plotly_figure.RSI(data1, num_period), use_container_width=True)
    
    if chart_type == "Candle" and indicator == "MACD":
        st.plotly_chart(plotly_figure.candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(plotly_figure.MACD(data1, num_period), use_container_width=True)
    
    if chart_type == "Line" and indicator == "RSI":
        st.plotly_chart(plotly_figure.close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(plotly_figure.RSI(data1, num_period), use_container_width=True)
    
    if chart_type == "Line" and indicator == "Moving Average":
        st.plotly_chart(plotly_figure.Moving_average(new_df1, num_period), use_container_width=True)
    
    if chart_type == "Line" and indicator == "MACD":
        st.plotly_chart(plotly_figure.close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(plotly_figure.MACD(data1, num_period), use_container_width=True)

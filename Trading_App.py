import streamlit as st
import numpy as np
npNaN = np.nan
st.set_page_config(page_title="Trading App", 
                   layout="wide", 
                   page_icon="💹")

st.title("Trading Guide App")
st.header("A Platform to Learn and Practice Trading Strategies.")
st.image("image.jpg")
st.markdown("## Wr provide the following features:")
st.markdown("### :one: Stock Information")
st.write("You can get detailed information about various stocks, including historical data, financial metrics, and news updates.")
st.markdown("### :two: Stock Prediction")
st.write("You can use machine learning models to predict future stock prices based on historical data.")
st.markdown("### :three: CAPM Return")
st.write("You can calculate the expected return of a stock using the Capital Asset Pricing Model (CAPM).")
st.markdown("### :four: CAPM Beta")
st.write("You can calculate the beta of a stock, which measures its volatility relative to the market.")

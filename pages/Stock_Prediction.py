import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling

import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average

st.set_page_config(page_title="Stock Prediction", layout="wide", page_icon="📈")

st.title("Stock Price Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input("Enter Stock Ticker", value="AAPL")

rmse = 0

st.subheader("Predicted Stock Prices for Next 30 Days : "+ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data , differencing_order)

st.write(f"Model RMSE: {rmse}")

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
st.write("Forecasted Closing Prices for Next 30 Days")
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])

if len(forecast) >= 30:
    st.plotly_chart(Moving_average(forecast.tail(30), num_period=30), use_container_width=True)
else:
    st.warning("Not enough data to plot moving average. Try increasing the data range or check your input.")

import dateutil
import datetime
import plotly.graph_objects as go
import numpy as np
npNaN = np.nan

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>"] + ["<b>" + str(i)[:10] + "<b>" for i in dataframe.columns],
            line_color='#0078ff', fill_color="#0078ff",
            align='center', font=dict(color='white', size=15), height=35,
        ),
        cells=dict(
            values=[["<b>" + str(i) + "<b>" for i in dataframe.index]] + [dataframe[i] for i in dataframe.columns],
            fill_color=[[rowOddColor, rowEvenColor] * len(dataframe)],
            align='left', line_color=['white'], font=dict(color='black', size=15)
        )
    )])
    fig.update_layout(height=400, margin=dict(l=0,r=0,b=0,t=0))
    return fig

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
        
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)

    elif num_period == 'YTD':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)

    else:
        if len(dataframe.index) == 0:
            return dataframe  # Return empty dataframe if no data
        date = dataframe.index[0]
    
    df_reset = dataframe.reset_index()
    # Ensure the date column is named 'Date'
    if df_reset.columns[0] != 'Date':
        df_reset = df_reset.rename(columns={df_reset.columns[0]: 'Date'})
    return df_reset[df_reset['Date'] >= date]

def close_chart(dataframe, num_period = False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line=dict(color='#5ab7ff', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(color='black', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line=dict(color='#0078ff', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line=dict(color='red', width=2)))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(margin=dict(l=0,r=20,b=0,t=20), height=500, plot_bgcolor='white', paper_bgcolor='#e1efff',legend=dict(yanchor="top", y=0.99, xanchor="left"))
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure(data=[go.Candlestick(x=dataframe['Date'],
                open=dataframe['Open'], high=dataframe['High'],
                low=dataframe['Low'], close=dataframe['Close'],
                increasing_line_color='#0078ff', decreasing_line_color='red')])
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(margin=dict(l=0,r=20,b=0,t=20), height=500, plot_bgcolor='white', paper_bgcolor='#e1efff',legend=dict(yanchor="top", y=0.99, xanchor="left"))
    return fig

def RSI(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    delta = dataframe['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    dataframe['RSI'] = rsi

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['RSI'], mode='lines', name='RSI', line=dict(color='#0078ff', width=2)))
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    fig.update_yaxes(range=[0,100])
    fig.update_layout(margin=dict(l=0,r=20,b=0,t=20), height=300, plot_bgcolor='white', paper_bgcolor='#e1efff',legend=dict(yanchor="top", y=0.99, xanchor="left"))
    return fig

def MACD(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    exp1 = dataframe['Close'].ewm(span=12, adjust=False).mean()
    exp2 = dataframe['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    dataframe['MACD'] = macd
    dataframe['Signal Line'] = signal

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'], mode='lines', name='MACD', line=dict(color='#0078ff', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Signal Line'], mode='lines', name='Signal Line', line=dict(color='red', width=2)))
    fig.update_layout(margin=dict(l=0,r=20,b=0,t=20), height=300, plot_bgcolor='white', paper_bgcolor='#e1efff',legend=dict(yanchor="top", y=0.99, xanchor="left"))
    return fig

def moving_average(dataframe, window):
    return dataframe['Close'].rolling(window=window).mean()
def Moving_average(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    dataframe['MA20'] = moving_average(dataframe, 20)
    dataframe['MA50'] = moving_average(dataframe, 50)
    dataframe['MA100'] = moving_average(dataframe, 100)

    # Ensure the index is reset and the date column is named 'Date'
    dataframe = dataframe.reset_index()
    # Remove duplicate 'Date' columns if present
    dataframe = dataframe.loc[:, ~dataframe.columns.duplicated()]
    # Reorder columns to keep 'Date' first
    cols = dataframe.columns.tolist()
    if 'Date' in cols and cols[0] != 'Date':
        cols.remove('Date')
        cols = ['Date'] + cols
        dataframe = dataframe[cols]
    if dataframe.columns[0] != 'Date':
        dataframe = dataframe.rename(columns={dataframe.columns[0]: 'Date'})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line=dict(color='black', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MA20'], mode='lines', name='MA20', line=dict(color='#5ab7ff', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MA50'], mode='lines', name='MA50', line=dict(color='#0078ff', width=2)))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MA100'], mode='lines', name='MA100', line=dict(color='red', width=2)))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(margin=dict(l=0,r=20,b=0,t=20), height=500, plot_bgcolor='white', paper_bgcolor='#e1efff',legend=dict(yanchor="top", y=0.99, xanchor="left"))
    return fig


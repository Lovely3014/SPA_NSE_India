# stock_analysis_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Load data
def load_data():
    return pd.read_csv("../DataSets/Stockslive.csv").drop(columns=['Unnamed: 0'])

stock_data = load_data()

# Convert date column to datetime
stock_data['Date'] = stock_data['Date'].astype('datetime64[ns]')

# Create daily return column
stock_data['Daily_return'] = stock_data['Close'].pct_change()
stock_data['Daily_return'].fillna(0, inplace=True)

# Calculate volatility (standard deviation of the rolling window)
stock_data['Volatility'] = stock_data['Close'].rolling(window=20).std()
stock_data['Volatility'].fillna(0, inplace=True)

# Simple moving averages (SMA)
stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
stock_data['SMA_50'].fillna(0, inplace=True)
stock_data['SMA_200'].fillna(0, inplace=True)

# Cumulative returns
stock_data['Cumulative_returns'] = (1 + stock_data['Daily_return']).cumprod() - 1
stock_data['Cumulative_returns'].fillna(0, inplace=True)

# Streamlit app
st.title("Live Stock Data Analysis")

# Filter by category
category = st.selectbox("Select Category", stock_data['Category'].unique())

# Filter by symbol (after selecting category)
filtered_data = stock_data[stock_data['Category'] == category]
symbol = st.selectbox("Select Stock Symbol", filtered_data['Symbol'].unique())

# Filtered stock data for selected symbol
stock = stock_data[(stock_data['Category'] == category) & (stock_data['Symbol'] == symbol)]

st.subheader(f"Technical Analysis for {symbol}")

# Display key statistics in a table format
st.write("### Descriptive Stats")
st.dataframe(stock.describe())

# Line chart for closing price over time
st.write("### Closing Price Over Time")
plt.figure(figsize=(10, 6))
plt.plot(stock['Date'], stock['Close'], label='Close Price', color='blue')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title(f'{symbol} Closing Price Over Time')
st.pyplot(plt)

# Daily Return
st.write("### Daily Return Over Time")
plt.figure(figsize=(10, 6))
plt.plot(stock['Date'], stock['Daily_return'], label='Daily Return', color='green')
plt.xlabel('Date')
plt.ylabel('Daily Return')
plt.title(f'{symbol} Daily Return Over Time')
st.pyplot(plt)

# Volatility
st.write("### Volatility Over Time")
plt.figure(figsize=(10, 6))
plt.plot(stock['Date'], stock['Volatility'], label='Volatility', color='red')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.title(f'{symbol} Volatility Over Time')
st.pyplot(plt)

# Simple Moving Averages (SMA)
st.write("### SMA 50 vs SMA 200")
plt.figure(figsize=(10, 6))
plt.plot(stock['Date'], stock['SMA_50'], label='SMA 50', color='orange')
plt.plot(stock['Date'], stock['SMA_200'], label='SMA 200', color='purple')
plt.xlabel('Date')
plt.ylabel('SMA Value')
plt.title(f'{symbol} SMA 50 vs SMA 200')
plt.legend()
st.pyplot(plt)

# Cumulative Returns
st.write("### Cumulative Returns Over Time")
plt.figure(figsize=(10, 6))
plt.plot(stock['Date'], stock['Cumulative_returns'], label='Cumulative Returns', color='cyan')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.title(f'{symbol} Cumulative Returns Over Time')
st.pyplot(plt)

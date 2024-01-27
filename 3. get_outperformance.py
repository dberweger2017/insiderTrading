import pandas as pd
import yfinance as yf
from datetime import datetime as dt
from tqdm import tqdm
import json

consolidated_df = pd.read_csv("consolidated.csv")

# Get a list of all the unique tickers
tickers = consolidated_df['Ticker'].unique()
print(f"Number of tickers: {len(tickers)}")

# Get all the daily closing prices for each of the tickers from 2003 to today
# and store them in a dictionary
ticker_data = {}
for ticker in tqdm(tickers):
    try:
        ticker_data[ticker] = yf.download(ticker, start="2003-01-01", end=dt.today())['Close']
    except Exception as e:
        print("Error with ticker:", ticker)

# Convert it to pandas dataframe
ticker_data = pd.DataFrame.from_dict(ticker_data, orient='columns')

# Save the dataframe to a csv file
ticker_data.to_csv("ticker_data.csv")
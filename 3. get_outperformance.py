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

serializable_data = {key: {k.strftime('%Y-%m-%d %H:%M:%S') if isinstance(k, pd.Timestamp) else k: v for k, v in df.items()} for key, df in ticker_data.items()}
with open('ticker_data.json', 'w') as fp:
    json.dump(serializable_data, fp)

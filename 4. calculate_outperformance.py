from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tqdm import tqdm

# Function to calculate future price changes
def calculate_future_price_changes(trades_df, prices_df, days_list):
    # Ensure prices_df has 'Date' as a datetime index
    if 'Date' in prices_df.columns:
        prices_df['Date'] = pd.to_datetime(prices_df['Date'])
        prices_df.set_index('Date', inplace=True)

    # Ensure trades_df 'Trade Date' is in datetime format
    trades_df = trades_df.copy()
    trades_df['Filing Date'] = pd.to_datetime(trades_df['Filing Date']).dt.normalize()

    # Add columns for each specified day in the future
    for days in tqdm(days_list):
        trades_df[f'Change_{days}d'] = np.nan  # Initialize with NaN

        for idx, row in trades_df.iterrows():
            trade_date = row['Filing Date']
            ticker = row['Ticker']

            if ticker in prices_df.columns:
                future_date = trade_date + timedelta(days=days)
                try:
                    # Get the stock price on the trade date and future date
                    price_on_trade_date = prices_df.at[trade_date, ticker]
                    price_on_future_date = prices_df.at[future_date, ticker]
                    
                    # Calculate the price change
                    if not np.isnan(price_on_trade_date) and not np.isnan(price_on_future_date):
                        price_change = (price_on_future_date - price_on_trade_date) / price_on_trade_date
                        trades_df.at[idx, f'Change_{days}d'] = price_change
                except KeyError:
                    # Future date not in data
                    continue

    return trades_df

df = pd.read_csv("consolidated.csv", low_memory=False)
print("Number of trades:", len(df))
ticker_df = pd.read_csv("ticker_data.csv", low_memory=False)
print("Number of tickers:", len(ticker_df.columns))

print(f"We have data for {round(len(ticker_df)/len(df['Ticker'].unique()), 2)*100}% tickers")

# Specify the days for which we want to calculate the stock price changes
days_list = [5, 31, 128]

# Calculate the future price changes
updated_test_df = calculate_future_price_changes(df, ticker_df, days_list)

# Save the updated dataframe to a CSV file
updated_test_df.to_csv("consolidated_with_stock_data.csv", index=False)
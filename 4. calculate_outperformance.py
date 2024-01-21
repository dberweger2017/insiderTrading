import pandas as pd
import numpy as np
from tqdm import tqdm
import json

# Get the consolidated dataframe
consolidated_df = pd.read_csv("consolidated.csv")

# open the file and load the dictionary
with open('ticker_data.json', 'r') as fp:
    ticker_data = json.load(fp)

# convert the dictionary back to a pandas dataframe
ticker_data = {key: pd.DataFrame.from_dict(df, orient='index', columns=['Close']) for key, df in ticker_data.items()}

print(len(ticker_data))
# Remove the keys whose values are empty
ticker_data = {key: df for key, df in ticker_data.items() if not df.empty}
print(len(ticker_data))

def calculate_growth(df, ticker, days):
    if ticker in ticker_data:
        try:
            current_date = df['Filing Date']
            previous_date = current_date - pd.Timedelta(days=days)

            # Check if the previous date is within the valid range
            if previous_date in ticker_data[ticker].index:
                df[f'{days}d'] = (ticker_data[ticker].loc[current_date]['Close'] - ticker_data[ticker].loc[previous_date]['Close']) / ticker_data[ticker].loc[previous_date]['Close'] * 100
                print(f"{ticker} - {days}d: {df[f'{days}d']}")
            else:
                df[f'{days}d'] = np.nan
        except KeyError as e:
            print(f"KeyError: {e}")
            df[f'{days}d'] = np.nan
    else:
        df[f'{days}d'] = np.nan
    return df



# List of days for which you want to calculate growth
# days_list = [1, 2, 3, 4, 5, 10, 20, 30, 60, 120, 240, 360]
# days_list = [i for i in range(1, 366)]
days_list = [5, 10]
# Iterate over each day and apply calculate_growth function with tqdm

for days in tqdm(days_list, desc="Calculating Growth"):
    consolidated_df = consolidated_df.apply(lambda x: calculate_growth(x, x['Ticker'], days), axis=1)
    print(f"Finished {days}d")

# Save the dataframe to a csv file
consolidated_df.to_csv("consolidated_growth.csv", index=False)

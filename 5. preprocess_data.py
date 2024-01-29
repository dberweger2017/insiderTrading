import pandas as pd
from tqdm import tqdm
tqdm.pandas()

data = pd.read_csv("consolidated_with_stock_data.csv")

print("Number of trades:", len(data))

def convert_number(str):
    str = str.replace("%", "")
    str = str.replace("-", "")
    if str == "New" or str == ">999":
        number = 100
    else:
        number = float(str)
    number = number / 100
    if number > 1:
        number = 1
    return number

# Use progress_apply instead of apply
data["ΔOwn"] = data["ΔOwn"].progress_apply(convert_number)

def convert_value_to_number(str):
    str = str.replace("$", "")
    str = str.replace(",", "")
    number = float(str)
    return number

# calculate the days between
data["trade_delta"] = (pd.to_datetime(data["Filing Date"]) - pd.to_datetime(data["Trade Date"])).dt.days

# Use progress_apply here as well
data["Value"] = data["Value"].progress_apply(convert_value_to_number)

data["Interesting"] = data["ΔOwn"] * data["Value"]

#data = data[(data['Trade Type'] == 'P - Purchase') & (data['Value'] > 500_000) & (data['ΔOwn'] > 0.2)]
data = data[(data['Trade Type'] == 'P - Purchase') & (data['Value'] > 1_000_000)]

#drop the columns we don't need
no_need_columns = ["1d","1w","1m","6m"]
data.drop(columns=no_need_columns, inplace=True)

# save to csv
data.to_csv("consolidated_with_stock_data_preprocesed.csv", index=False)
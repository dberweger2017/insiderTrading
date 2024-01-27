import pandas as pd

data = pd.read_csv("consolidated_with_stock_data.csv")

# print the column names
print(data.columns)

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

data["ΔOwn"] = data["ΔOwn"].apply(convert_number)

def convert_value_to_number(str):
    str = str.replace("$", "")
    str = str.replace(",", "")
    number = float(str)
    return number

data["Value"] = data["Value"].apply(convert_value_to_number)

data["Interesting"] = data["ΔOwn"] * data["Value"]

# save to csv
data.to_csv("consolidated_with_stock_data_preprocesed.csv", index=False)
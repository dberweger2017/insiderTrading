import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import requests
from concurrent.futures import ThreadPoolExecutor
import os

if not os.path.exists('data'):
    os.makedirs('data')

def getStockData(start_date, end_date):
    start_str = start_date.strftime('%m%%2F%d%%2F%Y')
    end_str = end_date.strftime('%m%%2F%d%%2F%Y')
    #url = f"http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={end_str}+-+{start_str}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1"
    url = f"http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr={end_str}+-+{start_str}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=1"
    try:
        r = requests.get(url)
        dfs = pd.read_html(r.text)
        return dfs[-3]
    except Exception as e:
        print(f"Something went wrong {e}")

def saveData(i):
    start_date = datetime.now() - timedelta(days=i)
    data = getStockData(start_date, start_date)
    
    rename_dict = {col: col.replace('\xa0', ' ') for col in data.columns if type(col) is str}
    data.rename(columns=rename_dict, inplace=True)

    if len(data.columns) > 2:
        data.to_csv(f'data/{start_date.strftime("%Y-%m-%d")}.csv', index=False)

def main():
    with ThreadPoolExecutor() as executor:
        print(f"Using {executor._max_workers} workers.")
        list(tqdm(executor.map(saveData, range(9_000)), total=9_000))

if __name__ == "__main__":
    main()

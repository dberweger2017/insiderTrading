import os
import pandas as pd
from tqdm import tqdm

def consolidate_files(folder_path, output_file_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    consolidated_data = []
    
    for file in tqdm(all_files):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)

        consolidated_data.append(df)
    
    # Concatenate all the dataframes
    final_consolidated_df = pd.concat(consolidated_data, ignore_index=True).sort_values(by=['Filing Date'])
    
    # Save the consolidated data to a single CSV file
    final_consolidated_df.to_csv(output_file_path, index=False)

consolidate_files("data", "consolidated.csv")
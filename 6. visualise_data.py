import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'consolidated_with_stock_data_preprocesed.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Identifying all the "Change" columns
change_columns = [col for col in data.columns if col.startswith('Change')]

# Adding 'Interesting', 'Owned', 'ΔOwn', and 'Value' columns to the correlation analysis
columns_for_correlation = ['Interesting', 'Owned', 'ΔOwn', 'Value'] + change_columns

# Convert the selected columns to numeric, handling non-numeric entries
selected_data = data[columns_for_correlation].apply(pd.to_numeric, errors='coerce')

# Calculate the correlation matrix
correlation_matrix = selected_data.corr()
 
# Filter the correlation matrix to include correlations of 'Change' columns with 'Interesting', 'Owned', 'ΔOwn', and 'Value'
# and exclude correlations among themselves
filtered_corr_matrix = correlation_matrix.filter(items=['Interesting', 'Owned', 'ΔOwn', 'Value']).drop(labels=['Interesting', 'Owned', 'ΔOwn', 'Value'])

# Creating a heatmap for the filtered correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(filtered_corr_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap Including 'Interesting' Column")
plt.show()
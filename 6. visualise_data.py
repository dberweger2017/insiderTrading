import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'consolidated_with_stock_data_slice_preprocesed.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Identifying all the "Change" columns
change_columns = [col for col in data.columns if col.startswith('Change')]
change_columns_with_interesting = change_columns + ['Interesting']

# Adding 'Owned', 'ΔOwn', and 'Value' columns to the correlation analysis
additional_columns = ['Owned', 'ΔOwn', 'Value']
columns_to_correlate = change_columns_with_interesting + additional_columns

# Filter out non-numeric columns and calculate the correlation matrix
numeric_data = data[columns_to_correlate].apply(pd.to_numeric, errors='coerce')
correlation_matrix_extended = numeric_data.corr()

# Creating an extended heatmap for the correlation values
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix_extended, annot=True, cmap='coolwarm')
plt.title("Extended Correlation Heatmap")
plt.show()

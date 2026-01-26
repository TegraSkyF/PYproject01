import pandas as pd

# Load the generated CSV file
df = pd.read_csv('synthetic_traffic.csv')

print(f'Total rows: {len(df)}')
print(f'NaN values: {df.isnull().sum().sum()}')
print('\nSample of data:')
print(df.head(15))
print('\nData info:')
print(df.info())
print('\nBasic statistics:')
print(df.describe())

# Check for anomalies (values significantly higher than the mean)
mean_sessions = df['sessions'].mean()
std_sessions = df['sessions'].std()
high_values = df[df['sessions'] > mean_sessions + 2*std_sessions]
print(f'\nPotential anomalies (values > mean + 2*std): {len(high_values)}')
print(high_values.head())
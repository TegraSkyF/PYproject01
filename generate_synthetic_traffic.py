import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_traffic():
    """
    Generates synthetic website traffic data with the following characteristics:
    - Time range: 2022-01-01 to 2024-12-31 (3 years)
    - Base level: ~1500 sessions per day
    - Annual growth: 15% per year
    - Weekly seasonality: weekends 30% lower than weekdays, Monday peak
    - Yearly seasonality: summer (-20%), sales period (+40%)
    - Anomalies: 5-7 random spikes (2-3x normal values)
    - Data gaps: 2% randomly removed
    - Noise: ±5% of daily values
    """
    
    # Define the date range
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Initialize the dataframe
    df = pd.DataFrame({'date': dates})
    
    # Calculate base level with annual growth
    # Base is 1500, growing 15% annually
    days_since_start = (df['date'] - start_date).dt.days
    years_since_start = days_since_start / 365.25  # Account for leap years
    
    # Apply annual growth
    base_sessions = 1500 * (1.15 ** years_since_start)
    
    # Apply weekly seasonality
    # Weekends (Saturday=5, Sunday=6) are 30% lower, Monday (0) has a slight boost
    day_of_week = df['date'].dt.dayofweek
    weekly_factor = np.where(day_of_week.isin([5, 6]), 0.7, 1.0)  # Weekend factor
    
    # Slight Monday boost
    weekly_factor = np.where(day_of_week == 0, 1.05, weekly_factor)
    
    base_sessions *= weekly_factor
    
    # Apply yearly seasonality
    month = df['date'].dt.month
    # Summer months (June-August) have 20% less traffic
    summer_factor = np.where(month.isin([6, 7, 8]), 0.8, 1.0)
    # Sales period (November-December) has 40% more traffic
    sales_factor = np.where(month.isin([11, 12]), 1.4, 1.0)
    
    base_sessions *= summer_factor * sales_factor
    
    # Add noise (±5%)
    noise = np.random.normal(1.0, 0.05, len(df))  # Mean=1.0, std=0.05
    sessions_with_noise = base_sessions * noise
    
    # Ensure no negative values
    sessions_with_noise = np.maximum(sessions_with_noise, 0)
    
    # Insert 5-7 random spikes (2-3x normal values)
    num_spikes = random.randint(5, 7)
    spike_indices = random.sample(range(len(df)), num_spikes)
    
    for idx in spike_indices:
        # Multiply by a random factor between 2 and 3
        spike_multiplier = random.uniform(2.0, 3.0)
        sessions_with_noise[idx] *= spike_multiplier
    
    # Randomly remove 2% of values to simulate data gaps
    total_rows = len(df)
    num_missing = int(total_rows * 0.02)
    missing_indices = random.sample(range(total_rows), num_missing)
    
    sessions_final = sessions_with_noise.copy()
    sessions_final[missing_indices] = np.nan
    
    # Create the final dataframe
    df['sessions'] = sessions_final
    
    # Save to CSV
    df.to_csv('synthetic_traffic.csv', index=False)
    print(f"Generated {len(df)} rows of synthetic traffic data.")
    print(f"Added {num_spikes} anomalies/spikes.")
    print(f"Removed {num_missing} values to simulate data gaps (~2%).")
    print("Data saved to synthetic_traffic.csv")
    
    return df

if __name__ == "__main__":
    # Set random seed for reproducibility (optional)
    # np.random.seed(42)
    # random.seed(42)
    
    traffic_data = generate_synthetic_traffic()
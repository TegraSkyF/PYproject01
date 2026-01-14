"""
Refactored version of the data processing function.
This represents the "after" state with improved readability, decomposition, and efficiency.
"""

import pandas as pd
import numpy as np


def categorize_customer_segment(purchase_amount: pd.Series, frequency: pd.Series) -> pd.Series:
    """
    Categorizes customers into segments based on purchase amount and frequency.

    Args:
        purchase_amount: Series containing purchase amounts
        frequency: Series containing purchase frequencies

    Returns:
        Series with customer segments ('premium', 'standard', 'basic', 'trial')
    """
    conditions = [
        (purchase_amount > 200) & (frequency > 10),
        (purchase_amount > 100) & (frequency > 5),
        purchase_amount > 50
    ]
    choices = ['premium', 'standard', 'basic']
    
    return np.select(conditions, choices, default='trial')


def calculate_loyalty_score(purchase_amount: pd.Series, frequency: pd.Series, 
                          days_since_last_purchase: pd.Series) -> pd.Series:
    """
    Calculates loyalty score based on purchase behavior metrics.

    Args:
        purchase_amount: Series containing purchase amounts
        frequency: Series containing purchase frequencies
        days_since_last_purchase: Series containing days since last purchase

    Returns:
        Series with loyalty scores
    """
    # Base score based on purchase amount
    purchase_score = np.select(
        [purchase_amount > 150, purchase_amount > 75],
        [30, 20],
        default=10
    )
    
    # Frequency score
    frequency_score = np.select(
        [frequency > 8, frequency > 4],
        [25, 15],
        default=5
    )
    
    # Recency score (if available)
    recency_score = np.select(
        [(~days_since_last_purchase.isna()) & (days_since_last_purchase < 30),
         (~days_since_last_purchase.isna()) & (days_since_last_purchase < 90)],
        [20, 10],
        default=0
    )
    
    return purchase_score + frequency_score + recency_score


def flag_high_value_customers(purchase_amount: pd.Series, threshold: float = 100) -> pd.Series:
    """
    Flags customers with purchases above a certain threshold.

    Args:
        purchase_amount: Series containing purchase amounts
        threshold: Minimum amount to qualify as high-value (default: 100)

    Returns:
        Boolean Series indicating high-value customers
    """
    return purchase_amount > threshold


def calculate_overall_average(purchase_amount: pd.Series) -> float:
    """
    Calculates the average purchase amount across all non-null values.

    Args:
        purchase_amount: Series containing purchase amounts

    Returns:
        Average purchase amount
    """
    return purchase_amount.dropna().mean()


def process_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process customer data to calculate various metrics and segments.

    This function adds several calculated columns to the input DataFrame:
    - high_value_customer: Boolean flag for high-value customers
    - overall_avg_purchase: Average purchase amount across all customers
    - customer_segment: Customer segment based on purchase behavior
    - loyalty_score: Numerical loyalty score based on multiple factors

    Args:
        df: Input DataFrame with customer data including purchase_amount, 
            frequency, and days_since_last_purchase columns

    Returns:
        DataFrame with added calculated columns
    """
    # Create a copy to avoid modifying the original DataFrame
    processed_df = df.copy()
    
    # Add high-value customer flag
    processed_df['high_value_customer'] = flag_high_value_customers(
        processed_df['purchase_amount']
    )
    
    # Add overall average purchase amount
    overall_avg = calculate_overall_average(processed_df['purchase_amount'])
    processed_df['overall_avg_purchase'] = overall_avg
    
    # Add customer segments
    processed_df['customer_segment'] = categorize_customer_segment(
        processed_df['purchase_amount'],
        processed_df['frequency']
    )
    
    # Add loyalty scores
    processed_df['loyalty_score'] = calculate_loyalty_score(
        processed_df['purchase_amount'],
        processed_df['frequency'],
        processed_df['days_since_last_purchase']
    )
    
    return processed_df
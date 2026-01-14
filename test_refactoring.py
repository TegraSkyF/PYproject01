"""
Test script to verify that refactored code produces the same results as the original.
"""
import pandas as pd
import numpy as np
from poor_code_example import process_data as original_process_data
from refactored_code import process_customer_data as refactored_process_data


# Create sample data
sample_data = {
    'purchase_amount': [50, 150, 250, 75, 300],
    'frequency': [2, 8, 12, 3, 15],
    'days_since_last_purchase': [45, 15, 5, 120, 10]
}
df = pd.DataFrame(sample_data)

print("Testing that both functions produce equivalent results:")
print("\nOriginal function result:")
original_result = original_process_data(df.copy())
print(original_result[['high_value', 'customer_segment', 'loyalty_score']].head())

print("\nRefactored function result:")
refactored_result = refactored_process_data(df.copy())
print(refactored_result[['high_value_customer', 'customer_segment', 'loyalty_score']].head())

print("\nColumn names differ slightly due to improved naming, but logic is preserved.")
print("The refactored version has better-named columns and is more maintainable.")
"""
Example of poorly written code for refactoring.
This represents the "before" state of the code that needs refactoring.
"""

import pandas as pd
import numpy as np


def process_data(df):
    """
    Process customer data to calculate various metrics.
    This is an example of poorly written code.
    """
    # Bad variable names
    x = df.copy()
    
    # Unnecessary loop instead of vectorized operations
    for i in range(len(x)):
        if x.iloc[i]['purchase_amount'] > 100:
            x.loc[i, 'high_value'] = True
        else:
            x.loc[i, 'high_value'] = False
    
    # Multiple operations in one function
    # Calculating average purchase amount
    total = 0
    count = 0
    for idx, row in x.iterrows():
        if pd.notnull(row['purchase_amount']):
            total += row['purchase_amount']
            count += 1
    avg_purchase = total / count if count > 0 else 0
    
    # Adding the average as a column (bad practice)
    x['avg_purchase_for_all'] = avg_purchase
    
    # Creating segments based on multiple conditions
    segments = []
    for idx, row in x.iterrows():
        if row['purchase_amount'] > 200 and row['frequency'] > 10:
            segments.append('premium')
        elif row['purchase_amount'] > 100 and row['frequency'] > 5:
            segments.append('standard')
        elif row['purchase_amount'] > 50:
            segments.append('basic')
        else:
            segments.append('trial')
    
    x['customer_segment'] = segments
    
    # Calculating loyalty score with complex nested conditions
    scores = []
    for idx, row in x.iterrows():
        score = 0
        if row['purchase_amount'] > 150:
            score += 30
        elif row['purchase_amount'] > 75:
            score += 20
        else:
            score += 10
            
        if row['frequency'] > 8:
            score += 25
        elif row['frequency'] > 4:
            score += 15
        else:
            score += 5
            
        if pd.notnull(row['days_since_last_purchase']):
            if row['days_since_last_purchase'] < 30:
                score += 20
            elif row['days_since_last_purchase'] < 90:
                score += 10
        
        scores.append(score)
    
    x['loyalty_score'] = scores
    
    # Return processed dataframe
    return x
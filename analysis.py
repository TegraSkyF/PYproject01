"""
Module for performing data analysis and calculating KPIs.
"""

import pandas as pd


def calculate_kpis(df):
    """
    Calculate key performance indicators from a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame with columns like 'date',
                           'sessions', 'revenue', etc.

    Returns:
        dict: Dictionary containing calculated KPIs
    """
    if df.empty:
        return {
            "total_sessions": 0,
            "avg_sessions_per_day": 0,
            "total_revenue": 0,
            "avg_revenue_per_session": 0,
            "conversion_rate": 0,
        }

    # Handle missing values by filling with 0
    df_filled = df.fillna(0)

    total_sessions = df_filled.get("sessions", pd.Series()).sum()
    total_revenue = df_filled.get("revenue", pd.Series()).sum()

    # Calculate average sessions per day
    avg_sessions_per_day = (
        df_filled.get("sessions", pd.Series()).mean()
        if "sessions" in df_filled.columns
        else 0
    )

    # Calculate conversion rate if both sessions and conversions are present
    if "conversions" in df_filled.columns and "sessions" in df_filled.columns:
        conversion_rate = (
            (df_filled["conversions"].sum() / df_filled["sessions"].sum())
            * 100
            if df_filled["sessions"].sum() != 0
            else 0
        )
    else:
        conversion_rate = 0

    # Calculate average revenue per session
    avg_revenue_per_session = (
        total_revenue / total_sessions if total_sessions != 0 else 0
    )

    kpis = {
        "total_sessions": total_sessions,
        "avg_sessions_per_day": round(avg_sessions_per_day, 2),
        "total_revenue": total_revenue,
        "avg_revenue_per_session": round(avg_revenue_per_session, 2),
        "conversion_rate": round(conversion_rate, 2),
    }

    return kpis

"""
Unit tests for analysis.py module.
"""

import pandas as pd
import pytest
from analysis import calculate_kpis


@pytest.fixture
def sample_dataframe():
    """Fixture that creates a sample DataFrame for testing."""
    data = {
        "date": pd.date_range(start="2023-01-01", periods=5),
        "sessions": [100, 150, 200, 120, 180],
        "revenue": [1000, 1500, 2000, 1200, 1800],
        "conversions": [10, 15, 20, 12, 18],
    }
    return pd.DataFrame(data)


@pytest.fixture
def dataframe_with_missing_values():
    """Fixture that creates a DataFrame with missing values for testing."""
    data = {
        "date": pd.date_range(start="2023-01-01", periods=5),
        "sessions": [100, None, 200, 120, 180],
        "revenue": [1000, 1500, None, 1200, 1800],
        "conversions": [10, 15, 20, None, 18],
    }
    return pd.DataFrame(data)


def test_calculate_kpis_basic(sample_dataframe):
    """Test calculate_kpis function with a basic DataFrame."""
    result = calculate_kpis(sample_dataframe)

    expected = {
        "total_sessions": 750,  # 100+150+200+120+180
        "avg_sessions_per_day": 150.0,  # 750/5
        "total_revenue": 7500,  # 1000+1500+2000+1200+1800
        "avg_revenue_per_session": 10.0,  # 7500/750
        "conversion_rate": 10.0,  # (10+15+20+12+18)/(100+150+200+120+180)*100 = 75/750*100 = 10%
    }

    # Compare individual values to handle numpy types
    assert result["total_sessions"] == expected["total_sessions"]
    assert result["avg_sessions_per_day"] == expected["avg_sessions_per_day"]
    assert result["total_revenue"] == expected["total_revenue"]
    assert result["avg_revenue_per_session"] == expected["avg_revenue_per_session"]
    assert result["conversion_rate"] == expected["conversion_rate"]


def test_calculate_kpis_empty_dataframe():
    """Test calculate_kpis function with an empty DataFrame."""
    empty_df = pd.DataFrame()
    result = calculate_kpis(empty_df)

    expected = {
        "total_sessions": 0,
        "avg_sessions_per_day": 0,
        "total_revenue": 0,
        "avg_revenue_per_session": 0,
        "conversion_rate": 0,
    }

    assert result == expected


def test_calculate_kpis_with_missing_values(dataframe_with_missing_values):
    """Test calculate_kpis function with a DataFrame containing missing values."""
    result = calculate_kpis(dataframe_with_missing_values)

    # With missing values filled as 0:
    # sessions: [100, 0, 200, 120, 180] -> sum=600, mean=120.0
    # revenue: [1000, 1500, 0, 1200, 1800] -> sum=5500
    # conversions: [10, 15, 20, 0, 18] -> sum=63
    expected = {
        "total_sessions": 600,
        "avg_sessions_per_day": 120.0,
        "total_revenue": 5500,
        "avg_revenue_per_session": 9.17,  # 5500/600 ≈ 9.17
        "conversion_rate": 10.5,  # 63/600*100 = 10.5
    }

    # Round the result values for comparison due to floating point precision
    rounded_result = {
        k: round(v, 2) if isinstance(v, float) else v for k, v in result.items()
    }
    assert rounded_result == expected


def test_calculate_kpis_no_conversions_column():
    """Test calculate_kpis function when conversions column is missing."""
    data = {
        "date": pd.date_range(start="2023-01-01", periods=3),
        "sessions": [100, 150, 200],
        "revenue": [1000, 1500, 2000],
    }
    df = pd.DataFrame(data)
    result = calculate_kpis(df)

    expected_conversion_rate = 0  # Should be 0 when conversions column is missing
    assert result["conversion_rate"] == expected_conversion_rate


def test_calculate_kpis_zero_sessions():
    """Test calculate_kpis function when total sessions is zero."""
    data = {
        "date": pd.date_range(start="2023-01-01", periods=3),
        "sessions": [0, 0, 0],
        "revenue": [1000, 1500, 2000],
        "conversions": [0, 0, 0],
    }
    df = pd.DataFrame(data)
    result = calculate_kpis(df)

    # When sessions are 0, avg_revenue_per_session and conversion_rate should be 0
    assert result["avg_revenue_per_session"] == 0
    assert result["conversion_rate"] == 0

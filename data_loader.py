"""
Data loading and preparation utilities.
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """Load and prepare the dataset."""
    df = pd.read_csv("data_wrangling/3_clean_final/output.csv")

    # Calculate engagement ratio
    df["engagement_ratio"] = df["median_playtime"] / df["all_styles"]

    # Handle infinite and NaN values
    df["engagement_ratio"] = df["engagement_ratio"].replace(
        [float("inf"), -float("inf")], pd.NA
    )

    # Convert release_date to datetime
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["release_year"] = df["release_date"].dt.year

    # Add calculated columns
    df["release_decade"] = (df["release_year"] // 10) * 10

    # Calculate user score ratio
    df["user_score_ratio"] = df["user_positive"] / (
        df["user_positive"] + df["user_negative"]
    )
    df["user_score_ratio"] = df["user_score_ratio"].fillna(0)

    return df

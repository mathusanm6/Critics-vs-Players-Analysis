"""
Main application file for Critics vs Players Analysis.
This is the entry point for the Streamlit application.
"""

import streamlit as st

# Import modules
from session_state import initialize_session_state
from data_loader import load_data
from filters import apply_filters
from ui_components import (
    render_filter_selector,
    render_base_filters,
    render_optional_filters,
    render_reset_button,
)
from charts import render_engagement_chart, render_genre_chart


# Page configuration
st.set_page_config(
    page_title="Critics vs Players Analysis", page_icon="🎮", layout="wide"
)

# Add Font Awesome CSS
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """,
    unsafe_allow_html=True,
)

# Initialize session state
initialize_session_state()

# Title
st.markdown(
    '<h1><i class="fa fa-gamepad"></i> Critics vs Players - Video Game Analysis</h1>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Load the data
df = load_data()

# Sidebar for all filters
st.sidebar.markdown(
    '<h2><i class="fa fa-filter"></i> Filters</h2>', unsafe_allow_html=True
)

# Render filter selector
render_filter_selector()

# Render base filters (genre and critic score)
base_filter_state = render_base_filters(df)

# Render active optional filters
optional_filter_state = render_optional_filters(df)

# Combine all filter states
filter_state = {
    **base_filter_state,
    **optional_filter_state,
    "active_optional_filters": st.session_state.active_optional_filters,
}

# Render reset button
render_reset_button()

# Apply filters
df_filtered = apply_filters(df, filter_state)

# Display filter summary
st.markdown(
    f'<i class="fa fa-chart-bar"></i> **Showing {len(df_filtered):,} games** out of {len(df):,} total games '
    f"({len(df_filtered)/len(df)*100:.1f}%)",
    unsafe_allow_html=True,
)

# Render charts
render_engagement_chart(df_filtered)
render_genre_chart(df_filtered)

# Footer
st.markdown("---")
st.markdown("**Data Source:** Merged IGN, Steam, and HLTB datasets")

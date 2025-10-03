"""
Session state management for the application.
"""

import streamlit as st


def initialize_session_state():
    """Initialize all session state variables."""
    # Cross-chart selections
    if "selected_genres_from_chart2" not in st.session_state:
        st.session_state.selected_genres_from_chart2 = []

    if "selected_games_from_chart1" not in st.session_state:
        st.session_state.selected_games_from_chart1 = []

    # Chart-specific filters
    if "chart1_genre_filter" not in st.session_state:
        st.session_state.chart1_genre_filter = []

    if "chart2_genre_filter" not in st.session_state:
        st.session_state.chart2_genre_filter = []

    # Active filters tracking
    if "active_filter_count" not in st.session_state:
        st.session_state.active_filter_count = 0

    # Active optional filters
    if "active_optional_filters" not in st.session_state:
        st.session_state.active_optional_filters = []

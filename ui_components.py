"""
UI components for filters.
"""

import streamlit as st
from config import OPTIONAL_FILTERS, PRICE_CATEGORIES, FILTER_ICONS
from utils import sort_critic_phrases


def icon(name):
    """Render a Font Awesome icon using HTML."""
    return f'<i class="fa fa-{name}"></i>'


def icon_text(icon_name, text):
    """Render icon with text using HTML."""
    return f'<i class="fa fa-{icon_name}"></i> {text}'


def render_filter_selector():
    """Render the filter selector."""
    # Filter selector
    available_filters = [
        f
        for f in OPTIONAL_FILTERS.keys()
        if f not in st.session_state.active_optional_filters
    ]

    if available_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            filter_to_add = st.selectbox(
                "filter_add",
                options=[""] + available_filters,
                format_func=lambda x: (
                    OPTIONAL_FILTERS.get(x, "Add filter...") if x else "Add filter..."
                ),
                key="filter_selector",
                label_visibility="collapsed",
            )
        with col2:
            if st.button(
                "＋",
                key="add_filter_btn",
                help="Add filter",
                disabled=not filter_to_add,
            ):
                if filter_to_add:
                    st.session_state.active_optional_filters.append(filter_to_add)
                    st.rerun()


def render_base_filters(df):
    """Render base filters (genre and critic score) and return their values."""
    filter_values = {}

    st.sidebar.markdown("---")

    # Genre filter
    genres = sorted(df["genre"].dropna().unique())
    col1, col2 = st.sidebar.columns([5, 1])
    with col1:
        st.markdown('<i class="fa fa-gamepad"></i> **Genre**', unsafe_allow_html=True)
        selected_genres = st.sidebar.multiselect(
            "Genre",
            options=["All"] + genres,
            default=["All"],
            label_visibility="collapsed",
        )
    with col2:
        st.markdown("")  # For alignment
        if st.button("ⓘ", key="genre_help", help="Select genres to filter games"):
            pass

    if "All" not in selected_genres and len(selected_genres) == 0:
        selected_genres = ["All"]

    # Critic score filter
    col1, col2 = st.sidebar.columns([5, 1])
    with col1:
        st.markdown(
            '<i class="fa fa-star"></i> **Critic Score**', unsafe_allow_html=True
        )
        critic_score_range = st.sidebar.slider(
            "Critic Score",
            min_value=0.0,
            max_value=10.0,
            value=(0.0, 10.0),
            step=0.1,
            format="%.2f",
            label_visibility="collapsed",
        )
    with col2:
        st.markdown("")  # For alignment
        if st.button("ⓘ", key="critic_help", help="Filter by critic score range"):
            pass

    filter_values["selected_genres"] = selected_genres
    filter_values["critic_score_range"] = critic_score_range
    filter_values["min_critic"] = 0.0
    filter_values["max_critic"] = 10.0

    # Engagement ratio filter (mandatory)
    col1, col2 = st.sidebar.columns([5, 1])
    with col1:
        st.markdown(
            '<i class="fa fa-chart-line"></i> **Engagement**', unsafe_allow_html=True
        )
        filter_values["engagement_range"] = st.sidebar.slider(
            "Engagement (K%)",
            min_value=-0.5,
            max_value=50.0,
            value=(-0.5, 50.0),
            step=0.5,
            format="%.1fK%%",
            key="engagement_filter",
            label_visibility="collapsed",
        )
    with col2:
        st.markdown("")  # For alignment
        if st.button("ⓘ", key="engagement_help", help="Filter by engagement ratio"):
            pass

    st.sidebar.markdown("---")

    return filter_values


def render_optional_filters(df):
    """Render all active optional filters and return their values."""
    filter_values = {}

    # Developer filter
    if "developer" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-code"></i> **Developer**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_developer", help="Remove"):
                st.session_state.active_optional_filters.remove("developer")
                st.rerun()

        developers = sorted(df["developer"].dropna().unique())
        filter_values["selected_developers"] = st.sidebar.multiselect(
            "Select developers",
            options=developers,
            default=[],
            key="developer_filter",
            label_visibility="collapsed",
        )
    else:
        filter_values["selected_developers"] = []

    # Publisher filter
    if "publisher" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-building"></i> **Publisher**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_publisher", help="Remove"):
                st.session_state.active_optional_filters.remove("publisher")
                st.rerun()

        publishers = sorted(df["publisher"].dropna().unique())
        filter_values["selected_publishers"] = st.sidebar.multiselect(
            "Select publishers",
            options=publishers,
            default=[],
            key="publisher_filter",
            label_visibility="collapsed",
        )
    else:
        filter_values["selected_publishers"] = []

    # Critic score phrase filter
    if "critic_phrases" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-comment"></i> **Critic Phrases**',
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("✕", key="remove_critic_phrases", help="Remove"):
                st.session_state.active_optional_filters.remove("critic_phrases")
                st.rerun()

        critic_phrases = sort_critic_phrases(
            df["critic_score_phrase"].dropna().unique()
        )
        filter_values["selected_phrases"] = st.sidebar.multiselect(
            "Select phrases",
            options=critic_phrases,
            default=critic_phrases,
            key="critic_phrases_filter",
            label_visibility="collapsed",
        )
    else:
        critic_phrases = sort_critic_phrases(
            df["critic_score_phrase"].dropna().unique()
        )
        filter_values["selected_phrases"] = critic_phrases

    # Age filter
    if "age" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-lock"></i> **Age (PEGI)**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_age", help="Remove"):
                st.session_state.active_optional_filters.remove("age")
                st.rerun()

        ages = sorted(df["required_age"].dropna().unique())
        filter_values["selected_ages"] = st.sidebar.multiselect(
            "Select ages",
            options=ages,
            default=ages,
            key="age_filter",
            label_visibility="collapsed",
        )
    else:
        ages = sorted(df["required_age"].dropna().unique())
        filter_values["selected_ages"] = ages

    # Price filter
    if "price" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-dollar-sign"></i> **Price**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_price", help="Remove"):
                st.session_state.active_optional_filters.remove("price")
                st.rerun()

        min_price = float(df["price"].min())
        max_price = float(df["price"].max())
        filter_values["price_range"] = st.sidebar.slider(
            "Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=1.0,
            key="price_range_filter",
            label_visibility="collapsed",
        )

        filter_values["price_categories"] = st.sidebar.multiselect(
            "Categories",
            options=PRICE_CATEGORIES,
            default=PRICE_CATEGORIES,
            key="price_categories_filter",
        )
    else:
        min_price = float(df["price"].min())
        max_price = float(df["price"].max())
        filter_values["price_range"] = (min_price, max_price)
        filter_values["price_categories"] = PRICE_CATEGORIES

    # Owners filter
    if "owners" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-users"></i> **Owners**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_owners", help="Remove"):
                st.session_state.active_optional_filters.remove("owners")
                st.rerun()

        owners_min = float(df["owners"].min())
        owners_max = float(df["owners"].max())
        filter_values["owners_range"] = st.sidebar.slider(
            "Number of Owners",
            min_value=owners_min,
            max_value=owners_max,
            value=(owners_min, owners_max),
            step=50000.0,
            format="%.0f",
            key="owners_filter",
            label_visibility="collapsed",
        )
    else:
        owners_min = float(df["owners"].min())
        owners_max = float(df["owners"].max())
        filter_values["owners_range"] = (owners_min, owners_max)

    # Playtime filter
    if "playtime" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-clock"></i> **Playtime**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_playtime", help="Remove"):
                st.session_state.active_optional_filters.remove("playtime")
                st.rerun()

        median_playtime_min = float(df["median_playtime"].min())
        median_playtime_max = float(df["median_playtime"].max())
        filter_values["median_playtime_range"] = st.sidebar.slider(
            "Median (hours)",
            min_value=median_playtime_min,
            max_value=median_playtime_max,
            value=(median_playtime_min, median_playtime_max),
            step=10.0,
            key="playtime_filter",
            label_visibility="collapsed",
        )
    else:
        median_playtime_min = float(df["median_playtime"].min())
        median_playtime_max = float(df["median_playtime"].max())
        filter_values["median_playtime_range"] = (
            median_playtime_min,
            median_playtime_max,
        )

    # Year filter
    if "year" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-calendar"></i> **Release Year**',
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("✕", key="remove_year", help="Remove"):
                st.session_state.active_optional_filters.remove("year")
                st.rerun()

        min_year = int(df["release_year"].min())
        max_year = int(df["release_year"].max())
        filter_values["year_range"] = st.sidebar.slider(
            "Year",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
            key="year_filter",
            label_visibility="collapsed",
        )
    else:
        min_year = int(df["release_year"].min())
        max_year = int(df["release_year"].max())
        filter_values["year_range"] = (min_year, max_year)

    # Decade filter
    if "decade" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-calendar-alt"></i> **Decade**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_decade", help="Remove"):
                st.session_state.active_optional_filters.remove("decade")
                st.rerun()

        decades = sorted(df["release_decade"].dropna().unique())
        selected_decades = st.sidebar.multiselect(
            "Select decades",
            options=[f"{int(d)}s" for d in decades],
            default=[f"{int(d)}s" for d in decades],
            key="decade_filter",
            label_visibility="collapsed",
        )
        filter_values["selected_decades_int"] = [
            int(d.replace("s", "")) for d in selected_decades
        ]
    else:
        filter_values["selected_decades_int"] = []

    # Minimum reviews filter
    if "min_reviews" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-edit"></i> **Min Reviews**', unsafe_allow_html=True
            )
        with col2:
            if st.button("✕", key="remove_min_reviews", help="Remove"):
                st.session_state.active_optional_filters.remove("min_reviews")
                st.rerun()

        filter_values["min_reviews"] = st.sidebar.number_input(
            "Minimum",
            min_value=0,
            max_value=int(df["user_positive"].max() + df["user_negative"].max()),
            value=0,
            step=100,
            key="min_reviews_filter",
            label_visibility="collapsed",
        )
    else:
        filter_values["min_reviews"] = 0

    # Min games per genre filter
    if "min_games_per_genre" in st.session_state.active_optional_filters:
        col1, col2 = st.sidebar.columns([5, 1])
        with col1:
            st.markdown(
                '<i class="fa fa-list-ol"></i> **Min Games per Genre**',
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("✕", key="remove_min_games_per_genre", help="Remove"):
                st.session_state.active_optional_filters.remove("min_games_per_genre")
                st.rerun()

        genre_counts = df["genre"].value_counts()
        max_count = int(genre_counts.max())
        filter_values["min_games_per_genre"] = st.sidebar.number_input(
            "Minimum games",
            min_value=1,
            max_value=max_count,
            value=1,
            step=1,
            key="min_games_per_genre_filter",
            label_visibility="collapsed",
            help="Filter out genres with fewer than this many games",
        )
    else:
        filter_values["min_games_per_genre"] = 1

    return filter_values


def render_reset_button():
    """Render the reset filters button."""
    if st.session_state.active_optional_filters:
        st.sidebar.markdown("---")
        if st.sidebar.button("↻ Reset", use_container_width=True):
            st.session_state.active_optional_filters = []
            st.rerun()

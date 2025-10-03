"""
Data filtering functions.
"""

from utils import categorize_price


def apply_filters(data, filter_state):
    """Apply all filters to the dataframe."""
    filtered = data.copy()

    # Genre filter
    selected_genres = filter_state.get("selected_genres", ["All"])
    if "All" not in selected_genres:
        filtered = filtered[filtered["genre"].isin(selected_genres)]

    # Developer filter
    selected_developers = filter_state.get("selected_developers", [])
    if selected_developers:
        filtered = filtered[filtered["developer"].isin(selected_developers)]

    # Publisher filter
    selected_publishers = filter_state.get("selected_publishers", [])
    if selected_publishers:
        filtered = filtered[filtered["publisher"].isin(selected_publishers)]

    # Critic score filters
    critic_score_range = filter_state.get("critic_score_range")
    if critic_score_range:
        filtered = filtered[
            (filtered["critic_score"] >= critic_score_range[0])
            & (filtered["critic_score"] <= critic_score_range[1])
        ]

    selected_phrases = filter_state.get("selected_phrases", [])
    if selected_phrases:
        filtered = filtered[filtered["critic_score_phrase"].isin(selected_phrases)]

    # User score filter
    user_score_range = filter_state.get("user_score_range", (0.0, 1.0))
    filtered = filtered[
        (filtered["user_score_ratio"] >= user_score_range[0])
        & (filtered["user_score_ratio"] <= user_score_range[1])
    ]

    # Age filter
    selected_ages = filter_state.get("selected_ages", [])
    active_optional_filters = filter_state.get("active_optional_filters", [])
    if "age" in active_optional_filters and selected_ages:
        filtered = filtered[filtered["required_age"].isin(selected_ages)]

    # Price filters
    if "price" in active_optional_filters:
        price_range = filter_state.get("price_range")
        if price_range:
            filtered = filtered[
                (filtered["price"] >= price_range[0])
                & (filtered["price"] <= price_range[1])
            ]

        # Price category filter
        price_categories = filter_state.get("price_categories", [])
        if price_categories:
            filtered["price_category"] = filtered["price"].apply(categorize_price)
            filtered = filtered[filtered["price_category"].isin(price_categories)]

    # Owners filter
    if "owners" in active_optional_filters:
        owners_range = filter_state.get("owners_range")
        if owners_range:
            filtered = filtered[
                (filtered["owners"] >= owners_range[0])
                & (filtered["owners"] <= owners_range[1])
            ]

    # Playtime filters
    if "playtime" in active_optional_filters:
        median_playtime_range = filter_state.get("median_playtime_range")
        if median_playtime_range:
            filtered = filtered[
                (filtered["median_playtime"] >= median_playtime_range[0])
                & (filtered["median_playtime"] <= median_playtime_range[1])
            ]

    # Engagement ratio filter
    if "engagement" in active_optional_filters:
        engagement_range = filter_state.get("engagement_range")
        if engagement_range:
            filtered = filtered[
                (filtered["engagement_ratio"] >= engagement_range[0])
                & (filtered["engagement_ratio"] <= engagement_range[1])
            ]

    # Year filters
    if "year" in active_optional_filters:
        year_range = filter_state.get("year_range")
        if year_range:
            filtered = filtered[
                (filtered["release_year"] >= year_range[0])
                & (filtered["release_year"] <= year_range[1])
            ]

    # Decade filter
    selected_decades_int = filter_state.get("selected_decades_int", [])
    if "decade" in active_optional_filters and selected_decades_int:
        filtered = filtered[filtered["release_decade"].isin(selected_decades_int)]

    # Minimum reviews filter
    if "min_reviews" in active_optional_filters:
        min_reviews = filter_state.get("min_reviews", 0)
        filtered["total_reviews"] = (
            filtered["user_positive"] + filtered["user_negative"]
        )
        filtered = filtered[filtered["total_reviews"] >= min_reviews]

    return filtered

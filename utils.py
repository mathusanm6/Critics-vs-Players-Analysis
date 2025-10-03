"""
Utility functions for the application.
"""

from config import CRITIC_RATING_ORDER, PRICE_CATEGORIES


def sort_critic_phrases(phrases):
    """Sort critic phrases according to the defined order."""
    # Create a mapping of phrase to its position in the order
    order_map = {phrase: i for i, phrase in enumerate(CRITIC_RATING_ORDER)}
    # Sort phrases based on their position, putting unknown phrases at the end
    return sorted(phrases, key=lambda x: order_map.get(x, len(CRITIC_RATING_ORDER)))


def categorize_price(price):
    """Categorize a price into predefined categories."""
    if price == 0:
        return "Free"
    elif price < 10:
        return "Budget (< $10)"
    elif price < 30:
        return "Standard ($10-$30)"
    elif price < 60:
        return "Premium ($30-$60)"
    else:
        return "Luxury (> $60)"


def count_active_filters(df_original, df_filtered, filter_state):
    """Count how many filters are actively reducing the dataset."""
    active_count = 0

    if "All" not in filter_state.get("selected_genres", ["All"]):
        active_count += 1
    if filter_state.get("selected_developers"):
        active_count += 1
    if filter_state.get("selected_publishers"):
        active_count += 1

    critic_score_range = filter_state.get("critic_score_range")
    if critic_score_range:
        min_critic = float(df_original["critic_score"].min())
        max_critic = float(df_original["critic_score"].max())
        if critic_score_range != (min_critic, max_critic):
            active_count += 1

    # Add more filter checks as needed
    return active_count

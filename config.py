"""
Configuration constants for the Critics vs Players application.
"""

# Load critic rating order from file
try:
    with open("critic_rating.txt", "r") as f:
        CRITIC_RATING_ORDER = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    # Fallback order if file not found
    CRITIC_RATING_ORDER = [
        "Masterpiece",
        "Amazing",
        "Great",
        "Good",
        "Okay",
        "Mediocre",
        "Bad",
        "Awful",
        "Painful",
        "Unbearable",
    ]

# Available optional filters (text only for dropdown)
OPTIONAL_FILTERS = {
    "developer": "Developer",
    "publisher": "Publisher",
    "critic_phrases": "Critic Score Phrases",
    "age": "Age Rating (PEGI)",
    "price": "Price",
    "owners": "Owners",
    "playtime": "Playtime",
    "engagement": "Engagement Ratio (% Difference)",
    "year": "Release Year",
    "decade": "Release Decade",
    "min_reviews": "Minimum Reviews",
    "min_games_per_genre": "Min Games per Genre",
}

# Filter icons mapping
FILTER_ICONS = {
    "developer": "code",
    "publisher": "building",
    "critic_phrases": "comment",
    "age": "lock",
    "price": "dollar-sign",
    "owners": "users",
    "playtime": "clock",
    "engagement": "chart-line",
    "year": "calendar",
    "decade": "calendar-alt",
    "min_reviews": "edit",
    "min_games_per_genre": "list-ol",
}

# Price categories
PRICE_CATEGORIES = [
    "Free",
    "Budget (< $10)",
    "Standard ($10-$30)",
    "Premium ($30-$60)",
    "Luxury (> $60)",
]

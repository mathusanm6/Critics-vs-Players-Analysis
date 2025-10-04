"""
Chart visualization functions.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from config import CRITIC_RATING_ORDER


def format_large_number(num):
    """Format large numbers with K for thousands and M for millions."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{num:.0f}"


def render_engagement_chart(df_filtered):
    """Render Chart 1: Impact of critic scores on player engagement."""
    st.header("1. Impact des critiques sur l'engagement")
    st.markdown(
        "**Engagement Ratio** = (median_playtime - all_styles) / all_styles  \n"
        "**Values in K%** - percentage in thousands (e.g., 0.02K% = 20%, 2K% = 2000%)  \n"
        "**Positive** = more engagement than expected | **Negative** = less engagement than expected"
    )

    # Use filtered data for Chart 1
    df_filtered_1 = df_filtered.copy()

    # Remove rows with missing values for the scatter plot
    df_filtered_1 = df_filtered_1.dropna(
        subset=["critic_score", "engagement_ratio", "owners"]
    )

    # Create scatter plot
    if len(df_filtered_1) > 0:
        # Convert to thousands: ratio * 100 (to %) / 1000 (to k) = ratio / 10
        df_filtered_1["engagement_thousands"] = df_filtered_1["engagement_ratio"] / 10

        # Apply square root scale to owners for better visualization
        # Square root is better than log for bubble charts - less aggressive compression
        df_filtered_1["owners_sqrt"] = np.sqrt(df_filtered_1["owners"])

        # Normalize the sqrt values to a reasonable range (e.g., 0-1)
        min_sqrt = df_filtered_1["owners_sqrt"].min()
        max_sqrt = df_filtered_1["owners_sqrt"].max()

        if max_sqrt > min_sqrt:
            # Normalize to 0-1 range, then scale to a reasonable size range
            df_filtered_1["owners_normalized"] = (
                df_filtered_1["owners_sqrt"] - min_sqrt
            ) / (max_sqrt - min_sqrt)
            # Scale to range from 0.1 to 1.0 for better size differentiation
            df_filtered_1["bubble_size"] = 0.1 + (
                df_filtered_1["owners_normalized"] * 0.9
            )
        else:
            # If all values are the same, use a constant size
            df_filtered_1["owners_normalized"] = 0.5
            df_filtered_1["bubble_size"] = 0.5

        fig1 = px.scatter(
            df_filtered_1,
            x="critic_score",
            y="engagement_thousands",
            size="bubble_size",
            color="critic_score_phrase",
            hover_data={
                "title": True,
                "price": ":.2f",
                "genre": True,
                "user_positive": True,
                "user_negative": True,
                "critic_score": ":.1f",
                "engagement_thousands": ":.2f",
                "median_playtime": ":.1f",
                "all_styles": ":.1f",
                "owners": ":,",
                "critic_score_phrase": False,
                "bubble_size": False,  # Hide the calculated bubble size
                "owners_sqrt": False,  # Hide the sqrt value
                "owners_normalized": False,  # Hide the normalized value
            },
            labels={
                "critic_score": "Critic Score",
                "engagement_thousands": "Engagement (%)",
                "median_playtime": "Median Playtime (hours)",
                "all_styles": "Expected Playtime (hours)",
                "owners": "Owners",
                "critic_score_phrase": "Critic Rating",
            },
            title="Impact of Critic Scores on Player Engagement",
            color_discrete_sequence=px.colors.qualitative.Set2,
            category_orders={"critic_score_phrase": CRITIC_RATING_ORDER},
            size_max=50,  # Adjusted for normalized logarithmic scale
        )

        # Update hover template to show 'k' suffix for engagement
        fig1.update_traces(
            hovertemplate="<br>".join(
                [
                    "<b>%{customdata[0]}</b>",
                    "Critic Score: %{x:.1f}",
                    "Engagement (%): %{y:.2f}k",
                    "Price: $%{customdata[1]:.2f}",
                    "Genre: %{customdata[2]}",
                    "Positive Reviews: %{customdata[3]:,}",
                    "Negative Reviews: %{customdata[4]:,}",
                    "Median Playtime: %{customdata[5]:.1f} hours",
                    "Expected Playtime: %{customdata[6]:.1f} hours",
                    "Owners: %{customdata[7]:,}",
                    "<extra></extra>",
                ]
            )
        )

        # Add horizontal line at y=0 to show expected engagement
        fig1.add_hline(
            y=0,
            line_dash="dash",
            line_color="gray",
            annotation_text="Expected Engagement",
            annotation_position="right",
        )

        fig1.update_layout(
            height=600,
            xaxis_title="Critic Score",
            yaxis_title="Engagement (%)",
            legend_title="Critic Rating",
        )

        # Calculate dynamic y-axis range based on data with 10% offset
        min_engagement = df_filtered_1["engagement_thousands"].min()
        max_engagement = df_filtered_1["engagement_thousands"].max()

        # Add 10% offset to both ends for better visualization
        y_range = max_engagement - min_engagement
        offset = y_range * 0.1 if y_range > 0 else 1

        y_min = min_engagement - offset
        y_max = max_engagement + offset

        # Ensure 0 is visible if it's within or near the range
        if y_min > 0:
            y_min = min(y_min, -offset)
        if y_max < 0:
            y_max = max(y_max, offset)

        # Update y-axis with the dynamic range and add k suffix (lowercase)
        fig1.update_yaxes(range=[y_min, y_max], ticksuffix="k")  # Display the chart
        st.plotly_chart(fig1, use_container_width=True)

        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Games Shown", len(df_filtered_1))
        with col2:
            st.metric("Avg Critic Score", f"{df_filtered_1['critic_score'].mean():.1f}")
        with col3:
            avg_engagement = df_filtered_1["engagement_ratio"].mean() / 10
            st.metric(
                "Avg Engagement",
                f"{avg_engagement:+.2f}K%",
                delta=f"{'Above' if avg_engagement > 0 else 'Below'} expected",
            )
        with col4:
            total_owners = df_filtered_1["owners"].sum()
            st.metric("Total Owners", format_large_number(total_owners))
    else:
        st.warning("No data available with the current filters.")

    st.markdown("---")


def render_genre_chart(df_filtered):
    """Render Chart 2: Genre and critic scores distribution."""
    st.header("2. Genre et critiques")

    # Use filtered data for Chart 2
    df_filtered_2 = df_filtered.copy()

    # Remove rows with missing critic scores
    df_filtered_2 = df_filtered_2.dropna(subset=["critic_score", "genre"])

    # Create box plot
    if len(df_filtered_2) > 0:
        # Calculate average critic score per genre (for metrics and annotations)
        genre_avg = df_filtered_2.groupby("genre")["critic_score"].mean()

        # Sort genres alphabetically
        genres_sorted = sorted(df_filtered_2["genre"].unique())
        df_filtered_2["genre"] = pd.Categorical(
            df_filtered_2["genre"], categories=genres_sorted, ordered=True
        )

        fig2 = px.box(
            df_filtered_2.sort_values("genre"),
            x="genre",
            y="critic_score",
            color="genre",
            hover_data={
                "title": True,
                "critic_score": ":.1f",
                "critic_score_phrase": True,
                "genre": False,
            },
            labels={"critic_score": "Critic Score", "genre": "Genre"},
            title="Distribution of Critic Scores by Genre",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )

        fig2.update_layout(
            height=600,
            xaxis_title="Genre",
            yaxis_title="Critic Score",
            showlegend=False,
            xaxis_tickangle=-45,
        )

        # Add average line for each genre
        for genre in genres_sorted:
            genre_data = df_filtered_2[df_filtered_2["genre"] == genre]
            avg_score = genre_data["critic_score"].mean()
            fig2.add_annotation(
                x=genre,
                y=avg_score,
                text=f"{avg_score:.1f}",
                showarrow=False,
                font=dict(size=10, color="black"),
                bgcolor="white",
                opacity=0.8,
            )

        # Display the chart
        st.plotly_chart(fig2, use_container_width=True)

        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Genres Shown", df_filtered_2["genre"].nunique())
        with col2:
            st.metric("Total Games", len(df_filtered_2))
        with col3:
            st.metric("Avg Critic Score", f"{df_filtered_2['critic_score'].mean():.1f}")
        with col4:
            best_genre = genre_avg.idxmax()
            st.metric("Best Genre", best_genre, f"{genre_avg.max():.1f}")

        # Show top 5 genres table
        st.subheader("📈 Top 5 Genres by Average Critic Score")
        top_genres = (
            df_filtered_2.groupby("genre")
            .agg({"critic_score": ["mean", "median", "count"], "owners": "sum"})
            .round(2)
        )
        top_genres.columns = [
            "Avg Score",
            "Median Score",
            "Number of Games",
            "Total Owners",
        ]
        top_genres = top_genres.sort_values("Avg Score", ascending=False).head(5)

        # Format the Total Owners column for better readability
        top_genres["Total Owners"] = top_genres["Total Owners"].apply(
            format_large_number
        )

        st.dataframe(top_genres, use_container_width=True)

    else:
        st.warning("No data available with the current filters.")

"""
Chart visualization functions.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from config import CRITIC_RATING_ORDER


def render_engagement_chart(df_filtered):
    """Render Chart 1: Impact of critic scores on player engagement."""
    st.header("1. 📊 Impact des critiques sur l'engagement")
    st.markdown(
        "**Engagement Ratio** = (median_playtime - all_styles) / all_styles  \n"
        "**Positive** = plus d'engagement que prévu | **Negative** = moins d'engagement que prévu"
    )

    # Use filtered data for Chart 1
    df_filtered_1 = df_filtered.copy()

    # Remove rows with missing values for the scatter plot
    df_filtered_1 = df_filtered_1.dropna(
        subset=["critic_score", "engagement_ratio", "owners"]
    )

    # Create scatter plot
    if len(df_filtered_1) > 0:
        # Multiply by 100 to convert to percentage for display
        df_filtered_1["engagement_percentage"] = df_filtered_1["engagement_ratio"] * 100

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
            df_filtered_1["bubble_size"] = 0.5

        fig1 = px.scatter(
            df_filtered_1,
            x="critic_score",
            y="engagement_percentage",
            size="bubble_size",
            color="critic_score_phrase",
            hover_data={
                "title": True,
                "price": ":.2f",
                "genre": True,
                "user_positive": True,
                "user_negative": True,
                "critic_score": ":.1f",
                "engagement_percentage": ":.1f",
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
                "engagement_percentage": "Engagement (% Difference from Expected)",
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
            yaxis_title="Engagement (% Difference from Expected)",
            legend_title="Critic Rating",
        )

        # Update y-axis to add percentage symbol and set reasonable range
        fig1.update_yaxes(ticksuffix="%", range=[-200, 500])  # -200% to +500%

        # Display the chart
        st.plotly_chart(fig1, use_container_width=True)

        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Games Shown", len(df_filtered_1))
        with col2:
            st.metric("Avg Critic Score", f"{df_filtered_1['critic_score'].mean():.1f}")
        with col3:
            avg_engagement = df_filtered_1["engagement_ratio"].mean() * 100
            st.metric(
                "Avg Engagement",
                f"{avg_engagement:+.1f}%",
                delta=f"{'Above' if avg_engagement > 0 else 'Below'} expected",
            )
        with col4:
            st.metric("Total Owners", f"{df_filtered_1['owners'].sum():,.0f}")
    else:
        st.warning("No data available with the current filters.")

    st.markdown("---")


def render_genre_chart(df_filtered):
    """Render Chart 2: Genre and critic scores distribution."""
    st.header("2. 📦 Genre et critiques")

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
        st.dataframe(top_genres, use_container_width=True)

    else:
        st.warning("No data available with the current filters.")

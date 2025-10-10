"""
Chart visualization functions.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from config import CRITIC_RATING_ORDER
from streamlit_plotly_events import plotly_events


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

    # Show genre selection status and clear button
    if st.session_state.selected_genres:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(
                f"Filtered by genres from chart: {', '.join(st.session_state.selected_genres)}"
            )
        with col2:
            if st.button("🔄 Clear Genre Selection", key="clear_genre_selection"):
                st.session_state.selected_genres = []
                st.session_state.genre_filter_disabled = False
                st.session_state.last_clicked_genre = None  # Reset click tracking
                st.rerun()

    # Use filtered data for Chart 1
    df_filtered_1 = df_filtered.copy()

    # Apply genre selection from chart 2 if active
    if st.session_state.selected_genres:
        df_filtered_1 = df_filtered_1[
            df_filtered_1["genre"].isin(st.session_state.selected_genres)
        ]

    # Remove rows with missing values for the scatter plot
    df_filtered_1 = df_filtered_1.dropna(
        subset=["critic_score", "engagement_ratio", "owners"]
    )

    # Create scatter plot
    if len(df_filtered_1) > 0:
        # Ensure numeric and normalize critic_score if needed
        df_filtered_1["critic_score"] = pd.to_numeric(
            df_filtered_1["critic_score"], errors="coerce"
        )

        # Auto-normalize if values look like 0–100
        if df_filtered_1["critic_score"].max() > 10:
            df_filtered_1["critic_score"] = df_filtered_1["critic_score"] / 10.0
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

    # Show instructions and clear button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(
            "💡 **Click on genre boxes below to highlight and filter the engagement chart above!**"
        )
        st.markdown(
            "*Tip: Click multiple genres to compare them. Click (Genre) Selection to clear.*"
        )
    with col2:
        if st.session_state.selected_genres:
            if st.button(
                "🔄 Clear Genre Selection",
                key="clear_genre_selection_chart",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state.selected_genres = []
                st.session_state.last_clicked_genre = None
                st.rerun()

    # Use filtered data for Chart 2
    df_filtered_2 = df_filtered.copy()

    # Remove rows with missing critic scores
    df_filtered_2 = df_filtered_2.dropna(subset=["critic_score", "genre"])

    # Create box plot
    if len(df_filtered_2) > 0:
        # Ensure numeric and normalize critic_score if needed
        df_filtered_2["critic_score"] = pd.to_numeric(
            df_filtered_2["critic_score"], errors="coerce"
        )

        # SAFETY CHECK: Only normalize if values are clearly in 0-100 range (not just > 10)
        # Changed threshold from 10 to 15 to avoid false positives with genre counts
        max_critic = df_filtered_2["critic_score"].max()
        min_critic = df_filtered_2["critic_score"].min()
        if max_critic > 15 and min_critic >= 0:
            df_filtered_2["critic_score"] = df_filtered_2["critic_score"] / 10.0

        # Calculate average critic score per genre (for metrics and annotations)
        genre_avg = df_filtered_2.groupby("genre")["critic_score"].mean()

        # Sort genres alphabetically
        genres_sorted = sorted(df_filtered_2["genre"].unique())
        df_filtered_2["genre"] = pd.Categorical(
            df_filtered_2["genre"], categories=genres_sorted, ordered=True
        )

        # Determine which genres to highlight
        if st.session_state.selected_genres:
            # Create a column to indicate selected genres
            df_filtered_2["is_selected"] = df_filtered_2["genre"].isin(
                st.session_state.selected_genres
            )
            df_filtered_2["genre_display"] = df_filtered_2["genre"].astype(str)
        else:
            df_filtered_2["is_selected"] = True
            df_filtered_2["genre_display"] = df_filtered_2["genre"].astype(str)

        fig2 = px.box(
            df_filtered_2.sort_values("genre"),
            x="genre",
            y="critic_score",
            color="genre",
            title="Distribution of Critic Scores by Genre",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )

        # Calculate statistics for each genre for annotations
        genre_stats = {}
        for genre in genres_sorted:
            genre_data = df_filtered_2[df_filtered_2["genre"] == genre]["critic_score"]
            genre_stats[genre] = {
                "min": genre_data.min(),
                "q1": genre_data.quantile(0.25),
                "median": genre_data.median(),
                "q3": genre_data.quantile(0.75),
                "max": genre_data.max(),
                "mean": genre_data.mean(),
            }

        # Enhanced hover template with all statistics
        fig2.update_traces(
            hovertemplate="<b>%{x}</b><br><br>"
            + "<b>Box Plot Statistics:</b><br>"
            + "━━━━━━━━━━━━━━━━<br>"
            + "Max: %{upperfence:.1f}<br>"
            + "Q3 (75%%): %{q3:.1f}<br>"
            + "Median: %{median:.1f}<br>"
            + "Q1 (25%%): %{q1:.1f}<br>"
            + "Min: %{lowerfence:.1f}<br>"
            + "<extra></extra>",
            boxmean=False,
        )

        fig2.update_layout(
            height=600,
            xaxis_title="Genre",
            yaxis_title="Critic Score",
            showlegend=False,
            xaxis_tickangle=-45,
            hoverlabel=dict(
                bgcolor="rgba(255, 255, 255, 0.95)",
                font_size=11,
                font_family="Courier New, monospace",
                bordercolor="gray",
            ),
        )

        # Make unselected genres appear faded if there's a selection
        if st.session_state.selected_genres:
            for trace in fig2.data:
                if trace.name not in st.session_state.selected_genres:
                    trace.update(opacity=0.3)

        # Use plotly_events to capture clicks on the chart
        selected_points = plotly_events(
            fig2,
            click_event=True,
            hover_event=False,
            select_event=False,
            override_height=600,
            override_width="100%",
            key="genre_chart",
        )

        # Handle click events with debouncing to prevent infinite loops
        if selected_points and len(selected_points) > 0:
            clicked_point = selected_points[0]

            if "x" in clicked_point:
                clicked_genre = clicked_point["x"]

                # Create a unique identifier for this click (genre + timestamp to ensure uniqueness)
                import time

                current_time = time.time()
                click_id = f"{clicked_genre}_{clicked_point.get('pointIndex', 0)}"

                # Only process if:
                # 1. This is a new click (different from last processed click)
                # 2. Or enough time has passed (more than 0.5 seconds)
                time_since_last = current_time - st.session_state.get(
                    "last_click_time", 0
                )

                if (st.session_state.last_clicked_genre != click_id) and (
                    time_since_last > 0.5
                ):
                    st.session_state.last_clicked_genre = click_id
                    st.session_state.last_click_time = current_time

                    # Toggle the genre selection
                    if clicked_genre in st.session_state.selected_genres:
                        st.session_state.selected_genres.remove(clicked_genre)
                        st.toast(f"❌ Deselected: {clicked_genre}", icon="🎮")
                    else:
                        # Add to selection
                        st.session_state.selected_genres.append(clicked_genre)
                        st.toast(f"✅ Selected: {clicked_genre}", icon="🎮")

                    st.rerun()

        # Show detailed statistics table for selected genres
        if st.session_state.selected_genres:
            st.markdown("---")
            st.subheader("📊 Detailed Statistics for Selected Genres")

            # Create statistics dataframe for selected genres
            stats_data = []
            for genre in st.session_state.selected_genres:
                if genre in genre_stats:
                    stats = genre_stats[genre]
                    stats_data.append(
                        {
                            "Genre": genre,
                            "Min": f"{stats['min']:.1f}",
                            "Q1 (25%)": f"{stats['q1']:.1f}",
                            "Median": f"{stats['median']:.1f}",
                            "Q3 (75%)": f"{stats['q3']:.1f}",
                            "Max": f"{stats['max']:.1f}",
                            "Average": f"{stats['mean']:.1f}",
                            "Games": len(
                                df_filtered_2[df_filtered_2["genre"] == genre]
                            ),
                        }
                    )

            if stats_data:
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(
                    stats_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Genre": st.column_config.TextColumn("Genre", width="medium"),
                        "Min": st.column_config.TextColumn("Min", width="small"),
                        "Q1 (25%)": st.column_config.TextColumn(
                            "Q1 (25%)", width="small"
                        ),
                        "Median": st.column_config.TextColumn("Median", width="small"),
                        "Q3 (75%)": st.column_config.TextColumn(
                            "Q3 (75%)", width="small"
                        ),
                        "Max": st.column_config.TextColumn("Max", width="small"),
                        "Average": st.column_config.TextColumn(
                            "Average ⭐", width="small"
                        ),
                        "Games": st.column_config.NumberColumn(
                            "# Games", width="small"
                        ),
                    },
                )

        # Show statistics
        st.markdown("---")

        # Determine which data to use for metrics
        if st.session_state.selected_genres:
            # Filter to show only selected genres
            df_for_metrics = df_filtered_2[
                df_filtered_2["genre"].isin(st.session_state.selected_genres)
            ]
            genre_avg_for_metrics = df_for_metrics.groupby("genre")[
                "critic_score"
            ].mean()
            metrics_title = f"Statistics for {len(st.session_state.selected_genres)} Selected Genre(s)"
        else:
            # Show all genres
            df_for_metrics = df_filtered_2
            genre_avg_for_metrics = genre_avg
            metrics_title = "Overall Statistics"

        st.markdown(f"**{metrics_title}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Genres Shown", df_for_metrics["genre"].nunique())
        with col2:
            st.metric("Total Games", len(df_for_metrics))
        with col3:
            st.metric(
                "Avg Critic Score", f"{df_for_metrics['critic_score'].mean():.1f}"
            )
        with col4:
            if len(genre_avg_for_metrics) > 0:
                best_genre = genre_avg_for_metrics.idxmax()
                st.metric(
                    "Best Genre", best_genre, f"{genre_avg_for_metrics.max():.1f}"
                )
            else:
                st.metric("Best Genre", "N/A", "0.0")

        # Show top genres table (or selected genres table)
        if st.session_state.selected_genres:
            st.subheader(f"📊 Selected Genres Overview")
            # Show only selected genres
            table_data = df_for_metrics
        else:
            st.subheader("📈 Top 5 Genres by Average Critic Score")
            # Show top 5
            table_data = df_filtered_2

        top_genres = (
            table_data.groupby("genre")
            .agg({"critic_score": ["mean", "median", "count"], "owners": "sum"})
            .round(2)
        )
        top_genres.columns = [
            "Avg Score",
            "Median Score",
            "Number of Games",
            "Total Owners",
        ]

        if st.session_state.selected_genres:
            # Show selected genres in the order they were selected
            top_genres = top_genres.loc[
                [g for g in st.session_state.selected_genres if g in top_genres.index]
            ]
        else:
            # Show top 5 by average score
            top_genres = top_genres.sort_values("Avg Score", ascending=False).head(5)

        # Format the Total Owners column for better readability
        top_genres["Total Owners"] = top_genres["Total Owners"].apply(
            format_large_number
        )

        st.dataframe(top_genres, use_container_width=True)

    else:
        st.warning("No data available with the current filters.")

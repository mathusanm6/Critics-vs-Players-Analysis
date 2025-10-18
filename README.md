# Critics vs Players: Should You Send Review Copies?

[![Open Data Pipeline](https://img.shields.io/badge/📊_Data_Pipeline-Open_Notebook-blue?style=for-the-badge)](./game_data_pipeline.ipynb) [![Open Analysis](https://img.shields.io/badge/📈_Critics_vs_Players-Open_Notebook-green?style=for-the-badge)](./critics_vs_players.ipynb)

**Data Pipeline**: ETL notebook that integrates IGN reviews, Steam metrics, and HowLongToBeat data into a unified dataset  
**Critics vs Players**: Interactive analysis exploring the relationship between critic scores, sales, and player engagement

---

**Business Question:** As a game publisher, is it worth sending review copies to critics? Does it drive sales and engagement?

**User Persona:** Thomas, game publisher about to launch a new PC (Windows) game on Steam after years of development.

---

## ⚠️ **Important Disclaimer: Toy Project**

> **This is a data science toy project for educational purposes only.**
>
> **Limitations:**
>
> - **Single critic source**: Only uses IGN reviews (not representative of all gaming critics)
> - **Platform limited**: Steam data for Windows PC games only (excludes consoles, Mac, Linux)
> - **Sample bias**: Dataset may not represent the full gaming market
> - **Not production-ready**: Do not use for actual business decisions without additional research
>
> For real business decisions, consult multiple review aggregators (Metacritic, OpenCritic), cross-platform data, and professional market research.

---

## Executive Summary

This analysis examines the relationship between critic scores, sales (owners), player engagement, and pricing to determine the ROI of critic reviews for PC game publishers.

**Key Finding:** Higher critic scores correlate with increased ownership and player engagement, but the effect varies significantly by genre and price point.

## 🔗 Data Sources

- [IGN Games Dataset](https://www.kaggle.com/datasets/joebeachcapital/ign-games) - Critics' ratings and reviews
- [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) - Player engagement and playtime statistics
- [HowLongToBeat](https://howlongtobeat.com/) - Game completion time data (via API)

## 📊 Dataset Overview

- **1,106 PC games** (2003-2016)
- **Sources:** IGN reviews + Steam metrics + HowLongToBeat data
- **Average critic score:** 7.51/10
- **Average ownership:** 1.32M copies
- **Match rate:** 61.4% between IGN and Steam catalogs

## Analysis Components

### 1. Data Pipeline (`game_data_pipeline.ipynb`)

Integrates three data sources into a unified dataset:

- **IGN:** Professional critic scores (0-10 scale)
- **Steam:** Sales (owners), playtime metrics, pricing
- **HowLongToBeat:** Completion rates as engagement proxy

**Pipeline metrics:**

- 18,625 IGN reviews → 2,332 PC games
- 27,075 Steam games → 1,433 matched
- 90.7% HLTB enrichment success

### 2. Business Analysis (`critics_vs_players.ipynb`)

Interactive visualizations answering:

- **Do higher scores = more sales?** Correlation analysis with p-values
- **Engagement Ratio:** Actual playtime vs expected completion time
- **Revenue Proxy:** Owners × Price as revenue indicator
- **Completion Ratio:** Main story time / Total playtime
- **Score Brackets:** Performance analysis across 6 score ranges (0-5, 5-6, 6-7, 7-8, 8-9, 9-10)

**Key Metrics:**

- **Engagement Ratio:** `median_playtime / all_styles` (>1 means overplaying)
- **Revenue Proxy:** `owners_midpoint × price` (estimated revenue)
- **Completion Ratio:** `main_story / median_playtime` (finishing rate)

## 🔧 Technical Implementation

### Requirements

```bash
pip install -r requirements.txt
```

### Quick Start

```bash
# 1. Run data pipeline
jupyter notebook game_data_pipeline.ipynb

# 2. Explore business insights
jupyter notebook critics_vs_players.ipynb
```

### Output Files

- `output/games_final_*.csv` - Cleaned dataset
- `output/quality_report_*.json` - Data quality metrics
- `logs/` - Processing diagnostics

## 📈 Visualizations

The analysis includes 8 interactive visualizations:

1. **Critic Score vs Sales (Owners)** - Scatter plot with trend line showing correlation between reviews and sales

   - Correlation > 0.3 = Strong positive relationship
   - Correlation > 0.1 = Weak positive relationship
   - Correlation ≤ 0.1 = No meaningful relationship

2. **Critic Score vs Player Engagement** - Engagement ratio analysis (playtime vs expected completion time)

   - Red line at 1.0 = Players match expected playtime

3. **Critic Score vs Revenue Potential** - Revenue proxy analysis with success quadrants

   - ✅ Success Zone: High score + High revenue
   - ⚠️ Hidden Gems: Low score + High revenue
   - ❓ Underperformers: High score + Low revenue

4. **Critic Score vs Completion Commitment** - How reviews relate to game completion rates

5. **Price vs Quality vs Sales** - 3D relationship colored by engagement

   - Size = ownership, Color = engagement ratio

6. **Performance by Score Bracket** - Bar chart with engagement overlay showing thresholds

   - Shows average owners and engagement by score range

7. **Critic Impact by Genre** - Faceted analysis for top 6 genres

   - 🔥 STRONG impact (r > 0.4)
   - ⚡ MODERATE impact (r > 0.2)
   - ⚠️ WEAK impact (r ≤ 0.2)

8. **Sales Distribution by Score** - Violin plots for risk analysis
   - Shows median, mean, variance by score bracket

## � Key Insights for Publishers

**Based on the analysis:**

- Critic scores show measurable correlation with sales (see visualization #1 for strength by genre)
- Score ≥7 shows significantly higher average ownership across most genres
- Genre matters: Some genres benefit more from critic attention than others (visualization #7)
- Risk consideration: Poor reviews can hurt more than no reviews (see score bracket performance)

**ROI Considerations:**

- **Costs:** Review copies + PR management + embargo coordination
- **Benefits:** Visibility boost, sales multiplier potential, platform featuring opportunities
- **Genre dependencies:** Impact varies significantly by genre (see faceted analysis)

## �🚫 What This Project Does NOT Cover

- Console market dynamics
- Multiple review sources (Metacritic, user reviews)
- Marketing spend impact
- Launch timing effects
- Regional differences
- Early Access strategies

## Methodology Notes

- **Fuzzy matching:** Handles title variations (85% similarity threshold)
- **DLC handling:** Consolidated with base games
- **Outlier detection:** Flags MMOs with extreme playtimes
- **Time period:** Pre-2016 (may not reflect current market)

## For Game Publishers

This analysis provides directional insights but should be combined with:

- Current market research
- Platform-specific data (consoles, Epic, etc.)
- Marketing budget considerations
- Target audience analysis
- Competitive landscape review

## 🔮 Future Improvements

- [ ] Add Metacritic aggregate scores
- [ ] Include user review sentiment
- [ ] Analyze review timing impact (pre vs post-launch)
- [ ] Add console data
- [ ] Machine learning model for ROI prediction

---

_Built to explore the publisher's dilemma: Are critic reviews worth the investment?_

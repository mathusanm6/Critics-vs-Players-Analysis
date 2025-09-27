\*# Critics vs Players: IGN Ratings, Steam Engagement & HowLongToBeat Analysis

This project analyzes the relationship between professional critics' ratings (from IGN), actual player engagement (from Steam), and game completion times (from HowLongToBeat).

## 🎯 Project Overview

Understanding the relationship between critical acclaim, player engagement, and game completion by connecting:

- **IGN Games Dataset**: Professional critics' ratings and reviews
- **Steam Games Dataset**: Player engagement metrics and playtime statistics
- **HowLongToBeat Dataset**: Game completion times for different play styles

## 📊 Key Questions

1. Do games with higher IGN critic scores have higher average/median playtime?
2. Which games are critically acclaimed but have low playtime engagement?
3. Which games have high playtime despite lower critical ratings?
4. How does completion time correlate with both ratings and playtime?
5. How do these relationships vary by genre?

## 🛠️ Setup

1. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the notebooks in sequence:

   ```bash
   # Step 1: Merge IGN and Steam data
   jupyter notebook 1_merge_ign_steam/merge_ign_steam.ipynb

   # Step 2: Add HowLongToBeat completion data
   jupyter notebook 2_merge_htlb/merge_htlb.ipynb
   ```

## 📁 Project Structure

```
Critics-vs-Players/
├── 1_merge_ign_steam/          # Step 1: IGN + Steam data merging
│   ├── merge_ign_steam.ipynb   # Data acquisition and merging notebook
│   └── output.csv              # Merged IGN + Steam dataset
├── 2_merge_htlb/               # Step 2: Add HowLongToBeat data
│   ├── input.csv               # Input dataset from step 1
│   ├── merge_htlb.ipynb        # HowLongToBeat data integration
│   └── output_modified.csv     # Final enriched dataset
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 📈 Analysis Workflow

1. **Data Acquisition** (Step 1)

   - Download IGN and Steam datasets from Kaggle
   - Load and explore dataset structures
   - Clean and prepare data for merging
   - Match games between IGN and Steam datasets
   - Export merged dataset

2. **Data Enrichment** (Step 2)

   - Load merged IGN + Steam dataset
   - Integrate HowLongToBeat API for completion time data
   - Process game titles for better API matching
   - Fetch completion times for multiple play styles (Main Story, Main + Extra, Completionist, All Styles)
   - Export final enriched dataset

3. **Analysis & Visualization** (Future steps)
   - Analyze correlations between critic ratings, playtime, and completion times
   - Identify patterns and outliers
   - Generate insights and visualizations

## 🔗 Data Sources

- [IGN Games Dataset](https://www.kaggle.com/datasets/joebeachcapital/ign-games) - Critics' ratings and reviews
- [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) - Player engagement and playtime statistics
- [HowLongToBeat](https://howlongtobeat.com/) - Game completion time data (via API)

## 📝 License

This project is for educational purposes as part of MSc coursework in Data Visualization.

-

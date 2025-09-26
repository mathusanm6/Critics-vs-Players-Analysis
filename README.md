# Critics vs Playtime: IGN Ratings and Steam Engagement Analysis

This project analyzes the relationship between professional critics' ratings (from IGN) and actual player engagement measured by playtime (from Steam).

## 🎯 Project Overview

Understanding whether critically acclaimed games correlate with higher player engagement by connecting:

- **IGN Games Dataset**: Professional critics' ratings and reviews
- **Steam Games Dataset**: Average and median playtime statistics

## 📊 Key Questions

1. Do games with higher IGN critic scores have higher average/median playtime?
2. Which games are critically acclaimed but have low playtime engagement?
3. Which games have high playtime despite lower critical ratings?
4. How does the rating-playtime relationship vary by genre?

## 🛠️ Setup

1. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the Jupyter notebook:
   ```bash
   jupyter notebook notebook.ipynb
   ```

## 📁 Project Structure

```
Critics-vs-Players/
├── notebook.ipynb      # Main analysis notebook
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 📈 Analysis Workflow

1. **Data Acquisition** - Download IGN and Steam datasets from Kaggle
2. **Data Loading** - Load and explore dataset structures
3. **Game Matching** - Match games between IGN and Steam datasets
4. **Analysis** - Analyze correlation between critic ratings and playtime
5. **Insights** - Identify patterns and relationships

## 🔗 Data Sources

- [IGN Games Dataset](https://www.kaggle.com/datasets/joebeachcapital/ign-games) - Critics' ratings
- [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) - Playtime statistics

## 📝 License

This project is for educational purposes as part of MSc coursework in Data Visualization.

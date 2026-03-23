# Bank Marketing Campaign ROI Analysis

> Who to Call, When to Call, and Why It Matters

## Overview

Analysis of a Portuguese bank's direct marketing campaigns (45,211 phone calls) to identify which customers are most likely to subscribe to a term deposit, optimize campaign strategy, and quantify the ROI impact of targeted vs. blanket marketing.

## Key Findings

- Only ~11% of customers subscribe — most marketing calls are wasted
- Targeted marketing using a predictive model can reduce costs by ~27% while retaining ~92% of conversions
- ROI improves from 368% to 489% with the targeted approach
- Calling more than 3 times shows diminishing returns
- Customers who converted in previous campaigns are the highest-value targets

## Project Structure

```
├── Marketing_ROI_Analysis.ipynb   # Full analysis notebook
├── blog_post.md                   # Summary article
├── data/raw/                      # Original dataset (not in repo)
├── data/cleaned/                  # Processed dataset
├── images/                        # Exported visualizations
├── requirements.txt               # Python dependencies
└── README.md
```

## Tech Stack

Python | Pandas | NumPy | Matplotlib | Seaborn | Scikit-learn

## How to Run

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download `bank-full.csv` from [Kaggle](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing) and place in `data/raw/`
4. Open and run: `jupyter notebook Marketing_ROI_Analysis.ipynb`

## Dataset

UCI Bank Marketing Dataset — 45,211 records of direct marketing campaigns (phone calls) by a Portuguese banking institution.

**Source:** [Kaggle](https://www.kaggle.com/datasets/henriqueyamahata/bank-marketing)

## Analysis Sections

1. **Data Loading & Inspection** — First look at 45K records
2. **Data Cleaning** — Handle unknowns, create useful features
3. **Exploratory Data Analysis** — Patterns, distributions, correlations
4. **Customer Segmentation** — Best and worst converting segments
5. **Campaign Optimization** — Timing, frequency, channel analysis
6. **Predictive Modeling** — Logistic Regression & Decision Tree (with data leakage comparison)
7. **ROI Analysis** — Business impact quantification and recommendations

## Author

Aspiring Data Analyst | Built with Python for portfolio demonstration

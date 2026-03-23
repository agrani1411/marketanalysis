# Bank Marketing Campaign ROI Analysis — Design Spec

## Overview

**Title:** "Bank Marketing Campaign ROI Analysis — Who to Call, When to Call, and Why It Matters"

**Goal:** Build a portfolio-grade data analytics project that demonstrates end-to-end analytical thinking — from data cleaning through predictive modeling to business recommendations — using the Bank Marketing Dataset.

**Target Audience:** Recruiters and hiring managers evaluating the author for data analyst roles.

**Dataset:** Bank Marketing Dataset (~45,000 records) from Kaggle (janiobachmann/bank-marketing-campaign-opening-a-term-deposit). Portuguese bank's direct marketing phone campaigns to sell term deposits.

## Data Acquisition

**File to use:** `bank-full.csv` (45,211 records, 17 columns) — the full version of the dataset.

**How to obtain:**
1. Download from Kaggle: visit the kernel page and download the dataset
2. Or via CLI: `python -m kaggle kernels pull janiobachmann/bank-marketing-campaign-opening-a-term-deposit`
3. Place the CSV file in `data/raw/bank-full.csv`

**Separator:** The file uses semicolons (`;`) as delimiters, not commas. Load with `pd.read_csv('data/raw/bank-full.csv', sep=';')`.

## Deliverables

1. **Jupyter Notebook** — The main analysis (`Marketing_ROI_Analysis.ipynb`)
2. **Blog Post** — ~800 word article for Medium/LinkedIn (`blog_post.md`)
3. **GitHub Repository** — Clean README, organized folder structure

### Future Additions (Phase 2 & 3)
- **Phase 2:** Plotly Dash interactive dashboard — customer segmentation filters, conversion funnel, ROI comparison visuals, and threshold slider. Deployed to Render for live portfolio link.
- **Phase 3:** SQL layer — load data into SQLite, write queries for aggregations/segmentation, feed results into Python for modeling

## Dataset Description

### Key Columns

**Customer attributes:**
- `age` — numeric
- `job` — categorical (admin, technician, management, etc.)
- `marital` — categorical (married, single, divorced)
- `education` — categorical (primary, secondary, tertiary)
- `default` — has credit in default? (yes/no)
- `balance` — average yearly balance in euros
- `housing` — has housing loan? (yes/no)
- `loan` — has personal loan? (yes/no)

**Campaign attributes:**
- `contact` — contact communication type (cellular, telephone, unknown)
- `day` — last contact day of the month
- `month` — last contact month
- `duration` — last contact duration in seconds
- `campaign` — number of contacts during this campaign
- `pdays` — days since last contact from previous campaign (-1 = not contacted)
- `previous` — number of contacts before this campaign
- `poutcome` — outcome of previous campaign (success, failure, other, unknown)

**Target variable:**
- `y` — has the client subscribed to a term deposit? (yes/no)

## Project Structure

```
marketanalysis/
├── data/
│   ├── raw/                          # Original Kaggle CSV
│   └── cleaned/                      # Processed data
├── images/                           # Exported charts for blog post
├── docs/
│   └── superpowers/
│       └── specs/                    # This spec and plans
├── Marketing_ROI_Analysis.ipynb      # Main analysis notebook
├── blog_post.md                      # Medium/LinkedIn article
├── requirements.txt                  # Python dependencies for reproducibility
└── README.md                         # Project overview for GitHub
```

## Tech Stack

- **Python 3** — core language
- **Pandas** — data loading, cleaning, manipulation
- **NumPy** — numerical operations
- **Matplotlib** — base plotting library
- **Seaborn** — statistical visualizations
- **Scikit-learn** — predictive modeling (Logistic Regression, Decision Tree)
- **Jupyter Notebook** — development and presentation environment

## Notebook Structure (7 Parts)

### Part 1: Setup & Data Loading
- Import all libraries
- Load CSV from `data/raw/`
- Display shape, dtypes, first/last 5 rows
- Basic info: row count, column count, memory usage
- **Skills shown:** Pandas basics, data inspection

### Part 2: Data Cleaning
- Check for missing values and handle them (impute or drop with justification)
- Fix data types (e.g., categorical columns)
- Check for duplicates
- Encode categorical variables where needed
- Save cleaned data to `data/cleaned/`
- **Skills shown:** Data wrangling, data quality assessment

### Part 3: Exploratory Data Analysis (EDA)
- Distribution of target variable (`y`) — class imbalance check
- Univariate analysis: histograms for numeric columns, bar charts for categorical
- Bivariate analysis: conversion rate by job, education, marital status, age group
- Correlation heatmap for numeric features
- Key statistical summaries
- **Skills shown:** Visualization, pattern recognition, statistical thinking

### Part 4: Customer Segmentation
- Group customers by job type, age brackets (18-30, 31-45, 46-60, 60+), education level, balance quartiles
- Calculate conversion rates per segment
- Identify top-performing segments (highest conversion rate)
- Identify worst-performing segments (lowest conversion rate, highest cost)
- Create a "customer persona" of the ideal target
- **Skills shown:** Business thinking, segmentation analysis

### Part 5: Campaign Optimization
- Analyze conversion rate by contact method (cellular vs telephone)
- Analyze conversion rate by month and day
- Impact of number of calls (campaign) on conversion — diminishing returns analysis
- Effect of previous campaign outcome on current conversion
- Effect of call duration on conversion (with caveat: duration is known only after the call)
- **Skills shown:** Analytical reasoning, operational insights

### Part 6: Predictive Modeling
- Train/test split (80/20)
- Handle class imbalance using `class_weight='balanced'` (keeps dependencies minimal)
- **Train two versions of each model:** one WITH `duration` and one WITHOUT `duration`
  - With duration: shows predictive power but not usable in practice (data leakage)
  - Without duration: the realistic model for actual campaign targeting
- Model 1: Logistic Regression (interpretable, baseline)
- Model 2: Decision Tree (visual, feature importance)
- Evaluation: accuracy, precision, recall, F1-score, confusion matrix, ROC-AUC
- Feature importance analysis
- Compare with/without duration results and explain the difference
- Use the WITHOUT-duration model for Part 7 ROI calculations
- **Skills shown:** Basic ML, model evaluation, feature importance, data leakage awareness

### Part 7: ROI Analysis & Business Recommendations
- Assume a cost-per-call (e.g., EUR 5 per call based on industry benchmarks)
- Assume a revenue-per-conversion (e.g., EUR 200 per term deposit based on average balance)
- Calculate current strategy cost: total calls x cost-per-call
- Calculate current revenue: total conversions x revenue-per-conversion
- Calculate current ROI
- Propose targeted strategy: use model to call only high-probability customers
- Calculate projected ROI of targeted strategy
- Quantify savings: "Bank saves X% of marketing budget while losing only Y% of conversions"
- Final 3-5 actionable recommendations
- **Skills shown:** Business impact quantification, ROI thinking, strategic recommendations

## Blog Post Structure (~800 words)

**Title:** "How a Bank Can Slash Its Marketing Budget — A Data Analysis" (update with actual % after Part 7 is complete)

1. **The Problem** (~150 words) — Bank calls 45,000 people, only ~11% subscribe. Most calls are wasted money.
2. **What the Data Tells Us** (~300 words) — 3-4 key findings with exported charts from the notebook
3. **The Solution** (~200 words) — Targeted strategy with projected ROI improvement
4. **What I Learned** (~150 words) — Personal reflection, tools used, link to GitHub

## Design Decisions

1. **Single notebook over multiple:** Beginner-friendly, recruiters see everything in one click, reads like a report.
2. **Logistic Regression + Decision Tree over complex models:** Interpretability matters more than accuracy for a business-focused project. These models can be explained to non-technical stakeholders.
3. **Assumed cost/revenue figures:** Real marketing cost data isn't in the dataset. Using industry benchmarks with clear disclaimers keeps the ROI analysis grounded and honest.
4. **Duration caveat:** Call duration is highly predictive but only known after the call. The analysis will flag this as a data leakage risk and show results with and without it.

## Success Criteria

- Notebook runs end-to-end without errors
- All charts are clear, labeled, and publication-ready
- Business recommendations are specific and quantified (not vague)
- Blog post is shareable on LinkedIn
- README clearly explains the project for recruiters
- Code has clear comments explaining what each section does (learning-friendly)

## Visualization Standards

- Use `plt.style.use('seaborn-v0_8')` for consistent styling
- Default figure size: `figsize=(10, 6)`
- All charts must have: title, axis labels, and legend where applicable
- Use a consistent color palette: `sns.color_palette('husl')` or similar
- Font size: title=14, axis labels=12, ticks=10

## Known Limitations & Caveats

1. **Duration leakage:** Call duration is only known after the call ends. Models including it are unrealistically accurate. The realistic model excludes it.
2. **Assumed costs:** Cost-per-call (EUR 5) and revenue-per-conversion (EUR 200) are industry estimates, not from the dataset. ROI numbers are illustrative, not precise.
3. **Historical data:** The dataset is from a Portuguese bank's past campaigns. Patterns may not generalize to other banks, countries, or time periods.
4. **No A/B test:** This is observational data, not an experiment. Correlations found do not prove causation.

## Learning Outcomes for the Author

By completing this project, the author will practice:
- Data cleaning with Pandas
- Visualization with Matplotlib/Seaborn
- Basic ML with Scikit-learn
- Business ROI thinking
- Technical writing (blog post)
- GitHub portfolio presentation

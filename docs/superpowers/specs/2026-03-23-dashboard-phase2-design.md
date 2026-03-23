# Bank Marketing ROI Dashboard — Phase 2 Design Spec

## Overview

**Title:** Interactive Marketing ROI Dashboard

**Goal:** Build a multi-tab interactive dashboard using Plotly Dash that lets users explore the bank marketing analysis through filters, charts, and an ROI threshold slider. Deploy to Render for a live portfolio link.

**Data Source:** `data/cleaned/bank-cleaned.csv` (produced by Phase 1 notebook)

**Target Audience:** Recruiters and hiring managers — the dashboard should be self-explanatory and visually polished.

## Tech Stack

- **Dash 2.x** — web application framework (by Plotly)
- **Dash Bootstrap Components** — layout and dark theme (`dbc.themes.DARKLY`)
- **Plotly** — interactive charts (hover tooltips, zoom, click)
- **Pandas** — data loading and transformation
- **Gunicorn** — production WSGI server for deployment
- **Render** — free-tier hosting (fallback: Railway or Hugging Face Spaces)

## Layout Design

**Layout C: Top Nav + Filter Bar**

- Pill-style horizontal tabs at the top for page navigation
- Global filter bar below tabs with dropdowns for Job, Age Group, Education
- Filters apply to the **active tab only** — when filters change, only the currently visible tab's callbacks fire. On tab switch, the active tab re-renders with current filter values. This avoids performance issues and circular callback errors.
- 4 KPI cards visible on every page (Total Customers, Conversion Rate, Targeted ROI, Cost Savings)
- KPI cards update when filters change
- Dark theme for modern look

## Dashboard Pages

### Page 1: Overview (Landing Page)
- **4 KPI cards** at top: Total Customers, Conversion Rate, Targeted ROI, Cost Savings
- **Subscription distribution** — Plotly pie/donut chart showing yes/no split
- **Conversion by job type** — horizontal bar chart
- **Key findings summary** — 3-4 bullet points as styled text cards
- All charts respond to global filters

### Page 2: Customer Segments
- **Conversion rate by segment** — grouped bar chart with dropdown to switch between: job, age group, education, marital status, balance group
- **Top 10 vs Bottom 10 segments** — side-by-side horizontal bar charts (age x job combos)
- **Ideal customer persona** — styled text card showing best value per dimension
- Charts respond to global filters

### Page 3: Campaign Optimization
- **Conversion rate by month** — line/bar chart
- **Call volume by month** — overlaid bar chart
- **Diminishing returns** — two stacked charts: conversion rate by # calls (bar) and customer count by # calls (line), sharing the same x-axis. Simpler than dual-axis and easier to read.
- **Contact method comparison** — bar chart (cellular vs telephone vs unknown)
- **Previous campaign outcome** — bar chart showing conversion rate by poutcome
- Charts respond to global filters

### Page 4: Model Performance
- **Model comparison table** — showing accuracy, precision, recall, F1, ROC-AUC for all 4 models
- **ROC curves** — Plotly line chart, side-by-side (with duration vs without duration)
- **Confusion matrix** — heatmap for the realistic LR model
- **Feature importance** — horizontal bar chart, top 15 features
- **Toggle switch** — with/without duration to highlight data leakage difference
- Note: Model results are pre-computed (we load saved predictions, not retrain live)

### Page 5: ROI Analysis (Star Feature)
- **Threshold slider** — draggable slider from 0.1 to 0.9
- When slider moves, ALL of these update in real-time:
  - KPI cards: calls made, conversions captured, cost, revenue, profit, ROI
  - Bar chart: current vs targeted strategy comparison
  - Text: "You save X% of calls while retaining Y% of conversions"
- **Strategy comparison table** — all thresholds side by side
- **Recommendations** — styled text cards with the 5 actionable recommendations

## Pre-computed Data

To avoid running ML models in the dashboard (slow, unnecessary), Phase 1 notebook must export these files (requires adding 1 cell to the notebook):

### `data/cleaned/bank-cleaned.csv` (already exists)

### `data/cleaned/model-predictions.csv` (new)
Columns:
- `y_test` — actual label (0/1)
- `y_prob_lr_wd` — LR with duration probabilities
- `y_prob_lr_nd` — LR no duration probabilities (used for ROI slider)
- `y_prob_dt_wd` — Decision Tree with duration probabilities
- `y_prob_dt_nd` — Decision Tree no duration probabilities
- `y_pred_lr_wd`, `y_pred_lr_nd`, `y_pred_dt_wd`, `y_pred_dt_nd` — class predictions

### `data/cleaned/model-metrics.json` (new)
```json
{
  "LR (with duration)": {"accuracy": 0.xx, "precision": 0.xx, "recall": 0.xx, "f1": 0.xx, "roc_auc": 0.xx},
  "LR (no duration)": {"accuracy": 0.xx, ...},
  "DT (with duration)": {...},
  "DT (no duration)": {...}
}
```

### `data/cleaned/feature-importance.csv` (new)
Columns: `feature`, `importance` — all features from the LR no-duration model, sorted by absolute coefficient value.

### ROI Constants
- `COST_PER_CALL = 5` (EUR)
- `REVENUE_PER_CONVERSION = 200` (EUR)
These are hardcoded in both the notebook (Part 7) and the dashboard (Page 5) for consistency.

## Project Structure

```
marketanalysis/
├── dashboard/
│   ├── __init__.py             # Makes dashboard a package
│   ├── app.py                  # Main Dash app: layout, dcc.Tabs, global callbacks
│   ├── data_loader.py          # Load CSVs and JSON once at startup
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── overview.py         # Overview tab layout + callbacks
│   │   ├── segments.py         # Segmentation tab
│   │   ├── campaign.py         # Campaign optimization tab
│   │   ├── model.py            # Model performance tab
│   │   └── roi.py              # ROI analysis tab with threshold slider
│   ├── components/
│   │   ├── __init__.py
│   │   ├── kpi_cards.py        # Reusable KPI card component
│   │   └── filters.py         # Global filter bar component
│   └── assets/
│       └── style.css           # Dark theme CSS
├── data/
│   └── cleaned/
│       ├── bank-cleaned.csv          # From Phase 1
│       ├── model-predictions.csv    # New: exported from notebook
│       ├── model-metrics.json       # New: exported from notebook
│       └── feature-importance.csv   # New: exported from notebook
├── requirements.txt            # Updated with dash, plotly, gunicorn
├── Procfile                    # For Render deployment
├── render.yaml                 # Render service config
└── ... (existing files)
```

## Architecture

**Tab pattern:** Use `dcc.Tabs` with `dcc.Tab` in a single `app.py`. Each page module exports a `layout()` function and registers its own callbacks. This is simpler than Dash's multi-page routing and avoids URL complexity for a beginner.

**Callback strategy:** Callbacks receive filter values as inputs. Only the active tab's callbacks fire because hidden tab content is not rendered (use `dcc.Tabs` with `content_style` or render content conditionally based on active tab). On tab switch, the selected tab's layout function is called with current filter values.

**Empty state handling:** When filters produce an empty DataFrame, charts show a "No data for selected filters" message and KPI cards display dashes instead of numbers.

## Styling

- **Dark theme** — use `dbc.themes.DARKLY` from Dash Bootstrap Components as the base theme
- **Additional colors:** dark background (#1a1a2e), dark cards (#16213e), accent blue (#0f3460)
- **KPI card colors:** green (#2ecc71), red (#e74c3c), blue (#3498db), yellow (#f39c12)
- **Chart template:** `plotly_dark`
- **Font:** System default sans-serif
- **Responsive:** Works on desktop and tablet (not mobile-optimized)

## Deployment

- **Render free tier** — web service, auto-deploy from GitHub
- `render.yaml` with build command: `pip install -r requirements.txt`
- Start command: `gunicorn dashboard.app:server`
- Environment: Python 3
- Data files included in repo (cleaned CSV is small ~4.5MB)
- **Fallback:** If Render free tier is unavailable, use Railway or Hugging Face Spaces

## Success Criteria

- Dashboard loads in under 3 seconds
- All 5 tabs work with interactive charts
- Global filters update all charts on the active page
- ROI threshold slider updates in real-time
- Deployed and accessible via a public URL
- Dark theme looks professional
- Charts have hover tooltips with data values

## Known Limitations

1. **No live model training** — predictions are pre-computed, dashboard only visualizes
2. **No mobile layout** — optimized for desktop/tablet only
3. **Free tier limits** — Render free tier may sleep after 15 min inactivity (first load takes ~30s to wake)
4. **Static data** — no database connection, reads CSV on startup

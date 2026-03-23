# Interactive Marketing ROI Dashboard — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 5-tab interactive Plotly Dash dashboard with global filters and an ROI threshold slider, then deploy to Render.

**Architecture:** Single Dash app using `dcc.Tabs` for navigation. Each tab is a separate module exporting a `layout()` function. Global filter bar and KPI cards are shared components. Data is pre-computed (CSVs + JSON) and loaded once at startup. Dark theme via Dash Bootstrap Components.

**Tech Stack:** Dash 2.x, Dash Bootstrap Components, Plotly, Pandas, Gunicorn

**Spec:** `docs/superpowers/specs/2026-03-23-dashboard-phase2-design.md`

---

## File Structure

```
marketanalysis/
├── dashboard/
│   ├── __init__.py             # Empty, makes it a package
│   ├── app.py                  # Main app: Dash init, layout with tabs, tab-switch callback
│   ├── data_loader.py          # Load all data files once at startup
│   ├── pages/
│   │   ├── __init__.py         # Empty
│   │   ├── overview.py         # Tab 1: KPIs + pie chart + job conversion bar
│   │   ├── segments.py         # Tab 2: segment analysis + top/bottom charts
│   │   ├── campaign.py         # Tab 3: monthly trends + diminishing returns
│   │   ├── model.py            # Tab 4: model comparison + ROC + feature importance
│   │   └── roi.py              # Tab 5: threshold slider + ROI calculator
│   ├── components/
│   │   ├── __init__.py         # Empty
│   │   ├── kpi_cards.py        # Reusable KPI card row
│   │   └── filters.py         # Global filter bar (job, age, education dropdowns)
│   └── assets/
│       └── style.css           # Custom dark theme overrides
├── requirements.txt            # Updated with dash dependencies
├── Procfile                    # Render start command
├── render.yaml                 # Render deployment config
└── data/cleaned/
    ├── bank-cleaned.csv        # Already exists
    ├── model-predictions.csv   # Created in Task 1
    ├── model-metrics.json      # Created in Task 1
    └── feature-importance.csv  # Created in Task 1
```

---

## Task 1: Export Model Data from Notebook

**Files:**
- Modify: `Marketing_ROI_Analysis.ipynb` (append 1 cell after Part 6, before Part 7)

- [ ] **Step 1: Add export cell to notebook**

Append this code cell after the feature importance cell (Part 6) and before the ROI section (Part 7):

```python
# Export model data for Phase 2 dashboard
import json

# 1. Export predictions
predictions_df = pd.DataFrame({
    'y_test': y_test.values,
    'y_prob_lr_wd': results['LR (with duration)']['y_prob'],
    'y_prob_lr_nd': results['LR (no duration)']['y_prob'],
    'y_prob_dt_wd': results['DT (with duration)']['y_prob'],
    'y_prob_dt_nd': results['DT (no duration)']['y_prob'],
    'y_pred_lr_wd': results['LR (with duration)']['y_pred'],
    'y_pred_lr_nd': results['LR (no duration)']['y_pred'],
    'y_pred_dt_wd': results['DT (with duration)']['y_pred'],
    'y_pred_dt_nd': results['DT (no duration)']['y_pred'],
})
predictions_df.to_csv('data/cleaned/model-predictions.csv', index=False)

# 2. Export metrics
metrics = {}
for name in results:
    metrics[name] = {
        'accuracy': results[name]['accuracy'],
        'precision': results[name]['precision'],
        'recall': results[name]['recall'],
        'f1': results[name]['f1'],
        'roc_auc': results[name]['roc_auc'],
    }
with open('data/cleaned/model-metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

# 3. Export feature importance
fi_df = pd.DataFrame({
    'feature': feature_importance.index,
    'importance': feature_importance.values
})
fi_df.to_csv('data/cleaned/feature-importance.csv', index=False)

print("Exported: model-predictions.csv, model-metrics.json, feature-importance.csv")
```

- [ ] **Step 2: Run notebook to generate exports**

Run: `cd "C:/Users/agran/agks/marketanalysis" && py -m nbconvert --to notebook --execute Marketing_ROI_Analysis.ipynb --output Marketing_ROI_Analysis.ipynb 2>&1`
Expected: No errors. Three new files in `data/cleaned/`.

- [ ] **Step 3: Verify exports**

Run: `ls -la data/cleaned/model-predictions.csv data/cleaned/model-metrics.json data/cleaned/feature-importance.csv`
Expected: All three files exist.

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add Marketing_ROI_Analysis.ipynb
git commit -m "feat: add model data export cell for Phase 2 dashboard"
```

---

## Task 2: Project Setup & Dependencies

**Files:**
- Modify: `requirements.txt`
- Create: `dashboard/__init__.py`
- Create: `dashboard/pages/__init__.py`
- Create: `dashboard/components/__init__.py`
- Create: `dashboard/assets/style.css`
- Create: `Procfile`
- Create: `render.yaml`
- Modify: `.gitignore`

- [ ] **Step 1: Update requirements.txt**

```
pandas==2.2.3
numpy==2.2.4
matplotlib==3.10.1
seaborn==0.13.2
scikit-learn==1.6.1
jupyter==1.1.1
dash>=4.0.0
dash-bootstrap-components>=1.6.0
plotly>=6.0.0
gunicorn>=23.0.0; sys_platform != "win32"
waitress>=3.0.0; sys_platform == "win32"
```

- [ ] **Step 2: Install new dependencies**

Run: `pip install dash dash-bootstrap-components plotly waitress`
Note: gunicorn is Linux-only (for Render deployment). Use waitress for local Windows testing.

- [ ] **Step 3: Create directory structure and __init__.py files**

Run:
```bash
cd "C:/Users/agran/agks/marketanalysis"
mkdir -p dashboard/pages dashboard/components dashboard/assets
touch dashboard/__init__.py dashboard/pages/__init__.py dashboard/components/__init__.py
```

- [ ] **Step 4: Create `dashboard/assets/style.css`**

```css
/* Custom dark theme overrides for Bank Marketing ROI Dashboard */

body {
    background-color: #1a1a2e !important;
    color: #e0e0e0 !important;
}

.nav-tabs .nav-link {
    color: #888 !important;
    border: 1px solid #333 !important;
    border-radius: 20px !important;
    margin: 0 4px;
    padding: 6px 16px;
    background: transparent;
}

.nav-tabs .nav-link.active {
    color: #fff !important;
    background-color: #0f3460 !important;
    border-color: #0f3460 !important;
}

.nav-tabs {
    border-bottom: none !important;
}

.kpi-card {
    background-color: #16213e;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    margin-bottom: 16px;
}

.kpi-card .kpi-value {
    font-size: 28px;
    font-weight: bold;
}

.kpi-card .kpi-label {
    font-size: 12px;
    color: #888;
    text-transform: uppercase;
    margin-top: 4px;
}

.filter-bar {
    background-color: #16213e;
    border-radius: 8px;
    padding: 12px 20px;
    margin-bottom: 20px;
}

.card-dark {
    background-color: #16213e;
    border: none;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}

.findings-card {
    background-color: #0f3460;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

.recommendation-card {
    background-color: #16213e;
    border-left: 4px solid #3498db;
    border-radius: 0 8px 8px 0;
    padding: 16px;
    margin-bottom: 12px;
}

/* Dropdown styling for dark theme */
.Select-control, .Select-menu-outer {
    background-color: #16213e !important;
    border-color: #333 !important;
}

.Select-value-label, .Select-placeholder {
    color: #e0e0e0 !important;
}
```

- [ ] **Step 5: Create `Procfile`**

```
web: gunicorn dashboard.app:server
```

- [ ] **Step 6: Create `render.yaml`**

```yaml
services:
  - type: web
    name: bank-marketing-dashboard
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn dashboard.app:server
    envVars:
      - key: PYTHON_VERSION
        value: "3.13"
```

- [ ] **Step 7: Add `.superpowers/` to `.gitignore`**

Append to `.gitignore`:
```
# Superpowers brainstorm files
.superpowers/
```

- [ ] **Step 8: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add requirements.txt dashboard/ Procfile render.yaml .gitignore
git commit -m "chore: Phase 2 setup — dash dependencies, project structure, deployment config"
```

---

## Task 3: Data Loader Module

**Files:**
- Create: `dashboard/data_loader.py`

- [ ] **Step 1: Create `dashboard/data_loader.py`**

```python
"""Load all data files once at startup."""
import os
import json
import pandas as pd

# Resolve paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')

# Load main dataset
df = pd.read_csv(os.path.join(DATA_DIR, 'bank-cleaned.csv'))

# Load model predictions
predictions = pd.read_csv(os.path.join(DATA_DIR, 'model-predictions.csv'))

# Load model metrics
with open(os.path.join(DATA_DIR, 'model-metrics.json'), 'r') as f:
    model_metrics = json.load(f)

# Load feature importance
feature_importance = pd.read_csv(os.path.join(DATA_DIR, 'feature-importance.csv'))

# ROI Constants (must match notebook Part 7)
COST_PER_CALL = 5
REVENUE_PER_CONVERSION = 200

# Filter options (for dropdowns)
JOB_OPTIONS = [{'label': 'All Jobs', 'value': 'All'}] + [
    {'label': j, 'value': j} for j in sorted(df['job'].unique())
]
AGE_OPTIONS = [{'label': 'All Ages', 'value': 'All'}] + [
    {'label': a, 'value': a} for a in ['18-30', '31-45', '46-60', '60+']
    if a in df['age_group'].unique()
]
EDUCATION_OPTIONS = [{'label': 'All Education', 'value': 'All'}] + [
    {'label': e, 'value': e} for e in sorted(df['education'].unique())
]


def filter_dataframe(job='All', age='All', education='All'):
    """Apply global filters to the main dataframe."""
    filtered = df.copy()
    if job != 'All':
        filtered = filtered[filtered['job'] == job]
    if age != 'All':
        filtered = filtered[filtered['age_group'] == age]
    if education != 'All':
        filtered = filtered[filtered['education'] == education]
    return filtered
```

- [ ] **Step 2: Test data loader**

Run: `cd "C:/Users/agran/agks/marketanalysis" && python -c "from dashboard.data_loader import df, predictions, model_metrics, feature_importance; print(f'Main: {df.shape}, Predictions: {predictions.shape}, Metrics: {len(model_metrics)} models, Features: {feature_importance.shape}')" 2>&1`
Expected: Prints shapes confirming all data loaded.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/data_loader.py
git commit -m "feat: add data loader module for dashboard"
```

---

## Task 4: Shared Components (KPI Cards + Filters)

**Files:**
- Create: `dashboard/components/kpi_cards.py`
- Create: `dashboard/components/filters.py`

- [ ] **Step 1: Create `dashboard/components/kpi_cards.py`**

```python
"""Reusable KPI card row component."""
from dash import html
import dash_bootstrap_components as dbc


def make_kpi_card(title, value, color):
    """Create a single KPI card."""
    return dbc.Col(
        html.Div([
            html.Div(value, className='kpi-value', style={'color': color}),
            html.Div(title, className='kpi-label'),
        ], className='kpi-card'),
        width=3,
    )


def kpi_row(total_customers, conversion_rate, targeted_roi, cost_savings):
    """Create a row of 4 KPI cards."""
    return dbc.Row([
        make_kpi_card('Total Customers', f'{total_customers:,}', '#2ecc71'),
        make_kpi_card('Conversion Rate', f'{conversion_rate:.1f}%', '#e74c3c'),
        make_kpi_card('Targeted ROI', f'{targeted_roi:.0f}%', '#3498db'),
        make_kpi_card('Cost Savings', f'{cost_savings:.0f}%', '#f39c12'),
    ], className='mb-3')


def empty_kpi_row():
    """KPI row for empty filter results."""
    return dbc.Row([
        make_kpi_card('Total Customers', '—', '#888'),
        make_kpi_card('Conversion Rate', '—', '#888'),
        make_kpi_card('Targeted ROI', '—', '#888'),
        make_kpi_card('Cost Savings', '—', '#888'),
    ], className='mb-3')
```

- [ ] **Step 2: Create `dashboard/components/filters.py`**

```python
"""Global filter bar component."""
from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard.data_loader import JOB_OPTIONS, AGE_OPTIONS, EDUCATION_OPTIONS


def filter_bar():
    """Create the global filter bar with dropdowns."""
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label('Job Type', style={'fontSize': '12px', 'color': '#888'}),
                dcc.Dropdown(
                    id='filter-job',
                    options=JOB_OPTIONS,
                    value='All',
                    clearable=False,
                    style={'backgroundColor': '#16213e'},
                ),
            ], width=3),
            dbc.Col([
                html.Label('Age Group', style={'fontSize': '12px', 'color': '#888'}),
                dcc.Dropdown(
                    id='filter-age',
                    options=AGE_OPTIONS,
                    value='All',
                    clearable=False,
                    style={'backgroundColor': '#16213e'},
                ),
            ], width=3),
            dbc.Col([
                html.Label('Education', style={'fontSize': '12px', 'color': '#888'}),
                dcc.Dropdown(
                    id='filter-education',
                    options=EDUCATION_OPTIONS,
                    value='All',
                    clearable=False,
                    style={'backgroundColor': '#16213e'},
                ),
            ], width=3),
            dbc.Col([
                html.Label('\u00a0', style={'fontSize': '12px'}),
                html.Div(
                    dbc.Button('Reset Filters', id='reset-filters', color='secondary', size='sm'),
                    className='d-grid',
                ),
            ], width=3),
        ]),
    ], className='filter-bar')
```

- [ ] **Step 3: Test imports**

Run: `cd "C:/Users/agran/agks/marketanalysis" && python -c "from dashboard.components.kpi_cards import kpi_row; from dashboard.components.filters import filter_bar; print('Components OK')" 2>&1`
Expected: "Components OK"

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/components/
git commit -m "feat: add KPI cards and filter bar components"
```

---

## Task 5: Overview Page (Tab 1)

**Files:**
- Create: `dashboard/pages/overview.py`

- [ ] **Step 1: Create `dashboard/pages/overview.py`**

```python
"""Overview tab — landing page with KPIs, pie chart, job conversion bar."""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from dashboard.data_loader import filter_dataframe, COST_PER_CALL, REVENUE_PER_CONVERSION, predictions


def layout(filtered_df):
    """Build overview tab layout from filtered data."""
    if filtered_df.empty:
        return html.Div("No data for selected filters.", className='card-dark',
                        style={'textAlign': 'center', 'padding': '40px'})

    total = len(filtered_df)
    conv_rate = filtered_df['y_numeric'].mean() * 100
    # Targeted ROI from predictions (uses full test set, not filtered)
    y_prob = predictions['y_prob_lr_nd']
    y_test = predictions['y_test']
    targeted_mask = y_prob >= 0.3
    t_calls = targeted_mask.sum()
    t_conv = y_test[targeted_mask].sum()
    t_cost = t_calls * COST_PER_CALL
    t_rev = t_conv * REVENUE_PER_CONVERSION
    targeted_roi = (t_rev - t_cost) / t_cost * 100 if t_cost > 0 else 0
    # Cost savings
    full_cost = len(y_test) * COST_PER_CALL
    cost_savings = (1 - t_cost / full_cost) * 100

    # Pie chart — subscription distribution
    sub_counts = filtered_df['y'].value_counts()
    pie_fig = go.Figure(go.Pie(
        labels=sub_counts.index,
        values=sub_counts.values,
        hole=0.4,
        marker=dict(colors=['#e74c3c', '#2ecc71']),
    ))
    pie_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        title='Subscription Distribution',
        font=dict(size=12),
        margin=dict(t=40, b=20, l=20, r=20),
    )

    # Bar chart — conversion by job type
    job_conv = filtered_df.groupby('job')['y_numeric'].agg(['mean', 'count']).reset_index()
    job_conv.columns = ['job', 'conversion_rate', 'count']
    job_conv = job_conv.sort_values('conversion_rate')
    bar_fig = px.bar(
        job_conv, x='conversion_rate', y='job', orientation='h',
        text=job_conv['conversion_rate'].apply(lambda x: f'{x*100:.1f}%'),
        labels={'conversion_rate': 'Conversion Rate', 'job': 'Job Type'},
        title='Conversion Rate by Job Type',
    )
    bar_fig.update_traces(marker_color='steelblue', textposition='outside')
    bar_fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        xaxis_tickformat='.0%',
        margin=dict(t=40, b=20, l=100, r=40),
    )

    # Key findings
    top_job = filtered_df.groupby('job')['y_numeric'].mean().idxmax()
    top_rate = filtered_df.groupby('job')['y_numeric'].mean().max() * 100
    avg_calls = filtered_df['campaign'].mean()

    return html.Div([
        # KPI row is rendered in app.py (shared across tabs)

        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=pie_fig, config={'displayModeBar': False}),
                ], className='card-dark'),
            ], width=5),
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=bar_fig, config={'displayModeBar': False}),
                ], className='card-dark'),
            ], width=7),
        ], className='mb-3'),

        html.H5('Key Findings', style={'color': '#fff', 'marginTop': '10px'}),
        html.Div([
            html.Div(f"Only {conv_rate:.1f}% of customers subscribe — most calls are wasted.",
                     className='findings-card'),
            html.Div(f"Best performing job: {top_job} ({top_rate:.1f}% conversion rate).",
                     className='findings-card'),
            html.Div(f"Average {avg_calls:.1f} calls per customer — diminishing returns after 3.",
                     className='findings-card'),
            html.Div(f"Targeted marketing can save ~{cost_savings:.0f}% of the budget.",
                     className='findings-card'),
        ]),
    ])
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/pages/overview.py
git commit -m "feat: add Overview page (Tab 1)"
```

---

## Task 6: Segments Page (Tab 2)

**Files:**
- Create: `dashboard/pages/segments.py`

- [ ] **Step 1: Create `dashboard/pages/segments.py`**

```python
"""Customer Segments tab — conversion by segment with dropdown, top/bottom segments."""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# Segment options for the dropdown
SEGMENT_OPTIONS = [
    {'label': 'Job Type', 'value': 'job'},
    {'label': 'Age Group', 'value': 'age_group'},
    {'label': 'Education', 'value': 'education'},
    {'label': 'Marital Status', 'value': 'marital'},
    {'label': 'Balance Group', 'value': 'balance_group'},
]


def build_segment_chart(filtered_df, segment_col):
    """Build a bar chart for the selected segment dimension."""
    title_map = {c['value']: c['label'] for c in SEGMENT_OPTIONS}
    title = title_map.get(segment_col, segment_col)
    seg = filtered_df.groupby(segment_col)['y_numeric'].mean().sort_values() * 100
    fig = px.bar(
        x=seg.values, y=seg.index, orientation='h',
        text=[f'{v:.1f}%' for v in seg.values],
        labels={'x': 'Conversion Rate (%)', 'y': title},
        title=f'Conversion Rate by {title}',
    )
    fig.update_traces(marker_color='steelblue', textposition='outside')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#16213e',
        plot_bgcolor='#16213e',
        margin=dict(t=40, b=20, l=120, r=40),
        height=400,
    )
    return fig


def layout(filtered_df):
    """Build segments tab layout."""
    if filtered_df.empty:
        return html.Div("No data for selected filters.", className='card-dark',
                        style={'textAlign': 'center', 'padding': '40px'})

    # Default segment chart (job)
    default_fig = build_segment_chart(filtered_df, 'job')

    # Top 10 / Bottom 10 cross-segments
    cross = filtered_df.groupby(['age_group', 'job'])['y_numeric'].agg(['mean', 'count']).reset_index()
    cross.columns = ['age_group', 'job', 'conversion_rate', 'count']
    cross = cross[cross['count'] >= 20]
    cross['label'] = cross['age_group'].astype(str) + ', ' + cross['job']
    cross = cross.sort_values('conversion_rate')

    if len(cross) >= 10:
        top10 = cross.tail(10)
        bottom10 = cross.head(10)

        top_fig = px.bar(
            top10, x='conversion_rate', y='label', orientation='h',
            text=top10['conversion_rate'].apply(lambda x: f'{x*100:.1f}%'),
            title='Top 10 Segments',
        )
        top_fig.update_traces(marker_color='#2ecc71', textposition='outside')
        top_fig.update_layout(
            template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
            xaxis_tickformat='.0%', margin=dict(t=40, b=20, l=140, r=40),
        )

        bottom_fig = px.bar(
            bottom10, x='conversion_rate', y='label', orientation='h',
            text=bottom10['conversion_rate'].apply(lambda x: f'{x*100:.1f}%'),
            title='Bottom 10 Segments',
        )
        bottom_fig.update_traces(marker_color='#e74c3c', textposition='outside')
        bottom_fig.update_layout(
            template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
            xaxis_tickformat='.0%', margin=dict(t=40, b=20, l=140, r=40),
        )
    else:
        top_fig = go.Figure()
        bottom_fig = go.Figure()
        top_fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                              title='Not enough segments (need min 20 per group)')
        bottom_fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e')

    # Ideal customer persona
    segments = {'job': 'Job', 'age_group': 'Age', 'education': 'Education',
                'marital': 'Marital', 'balance_group': 'Balance'}
    persona_items = []
    for col, title in segments.items():
        best = filtered_df.groupby(col)['y_numeric'].mean()
        if not best.empty:
            best_val = best.idxmax()
            best_rate = best.max() * 100
            persona_items.append(html.Div(
                f"{title}: {best_val} ({best_rate:.1f}%)",
                className='findings-card'
            ))

    return html.Div([
        # Segment dropdown + chart
        html.Div([
            html.Label('Select Segment Dimension:', style={'color': '#888', 'fontSize': '12px'}),
            dcc.Dropdown(
                id='segment-selector',
                options=SEGMENT_OPTIONS,
                value='job',
                clearable=False,
                style={'backgroundColor': '#16213e', 'marginBottom': '10px', 'width': '300px'},
            ),
            dcc.Graph(id='segment-chart', figure=default_fig, config={'displayModeBar': False}),
        ], className='card-dark mb-3'),

        # Top/Bottom segments
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(figure=top_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=6),
            dbc.Col(html.Div(dcc.Graph(figure=bottom_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=6),
        ], className='mb-3'),

        # Persona
        html.H5('Ideal Target Customer', style={'color': '#fff'}),
        html.Div(persona_items),
    ])


def register_callbacks(app):
    """Register segment dropdown callback."""
    from dash import callback, Output, Input, State
    from dashboard.data_loader import filter_dataframe

    @app.callback(
        Output('segment-chart', 'figure'),
        [Input('segment-selector', 'value'),
         Input('filter-job', 'value'),
         Input('filter-age', 'value'),
         Input('filter-education', 'value')],
    )
    def update_segment_chart(segment_col, job, age, education):
        filtered = filter_dataframe(job, age, education)
        if filtered.empty:
            fig = go.Figure()
            fig.update_layout(template='plotly_dark', paper_bgcolor='#16213e',
                              title='No data for selected filters')
            return fig
        return build_segment_chart(filtered, segment_col)
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/pages/segments.py
git commit -m "feat: add Segments page (Tab 2)"
```

---

## Task 7: Campaign Page (Tab 3)

**Files:**
- Create: `dashboard/pages/campaign.py`

- [ ] **Step 1: Create `dashboard/pages/campaign.py`**

```python
"""Campaign Optimization tab — monthly trends, diminishing returns, contact method."""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


def layout(filtered_df):
    """Build campaign optimization tab layout."""
    if filtered_df.empty:
        return html.Div("No data for selected filters.", className='card-dark',
                        style={'textAlign': 'center', 'padding': '40px'})

    month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    # Monthly conversion rate + volume
    monthly = filtered_df.groupby('month')['y_numeric'].agg(['mean', 'count']).reindex(month_order).dropna()
    monthly.columns = ['conversion_rate', 'count']

    month_conv_fig = go.Figure()
    month_conv_fig.add_trace(go.Bar(
        x=monthly.index, y=monthly['conversion_rate'] * 100,
        name='Conversion Rate (%)', marker_color='steelblue',
    ))
    month_conv_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        title='Conversion Rate by Month', yaxis_title='Conversion Rate (%)',
        margin=dict(t=40, b=20, l=60, r=20),
    )

    month_vol_fig = go.Figure()
    month_vol_fig.add_trace(go.Bar(
        x=monthly.index, y=monthly['count'],
        name='Call Volume', marker_color='coral',
    ))
    month_vol_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        title='Call Volume by Month', yaxis_title='Number of Calls',
        margin=dict(t=40, b=20, l=60, r=20),
    )

    # Diminishing returns — two stacked charts
    camp = filtered_df.groupby('campaign')['y_numeric'].agg(['mean', 'count']).reset_index()
    camp.columns = ['calls', 'conversion_rate', 'customer_count']
    camp = camp[camp['customer_count'] >= 20]

    dim_conv_fig = go.Figure()
    dim_conv_fig.add_trace(go.Bar(
        x=camp['calls'], y=camp['conversion_rate'] * 100,
        marker_color='steelblue', name='Conversion Rate',
    ))
    dim_conv_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        title='Conversion Rate by Number of Calls',
        xaxis_title='# Calls', yaxis_title='Conversion Rate (%)',
        margin=dict(t=40, b=10, l=60, r=20), height=250,
    )

    dim_count_fig = go.Figure()
    dim_count_fig.add_trace(go.Scatter(
        x=camp['calls'], y=camp['customer_count'],
        mode='lines+markers', marker_color='coral', name='Customers',
    ))
    dim_count_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        title='Customer Count by Number of Calls',
        xaxis_title='# Calls', yaxis_title='Customers',
        margin=dict(t=40, b=20, l=60, r=20), height=250,
    )

    # Contact method
    contact = filtered_df.groupby('contact')['y_numeric'].mean().sort_values() * 100
    contact_fig = px.bar(
        x=contact.values, y=contact.index, orientation='h',
        text=[f'{v:.1f}%' for v in contact.values],
        title='Conversion Rate by Contact Method',
        labels={'x': 'Conversion Rate (%)', 'y': 'Contact'},
    )
    contact_fig.update_traces(marker_color='steelblue', textposition='outside')
    contact_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        margin=dict(t=40, b=20, l=80, r=40),
    )

    # Previous campaign outcome
    poutcome = filtered_df.groupby('poutcome')['y_numeric'].mean().sort_values() * 100
    pout_fig = px.bar(
        x=poutcome.values, y=poutcome.index, orientation='h',
        text=[f'{v:.1f}%' for v in poutcome.values],
        title='Conversion by Previous Campaign Outcome',
        labels={'x': 'Conversion Rate (%)', 'y': 'Previous Outcome'},
    )
    pout_fig.update_traces(marker_color='steelblue', textposition='outside')
    pout_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        margin=dict(t=40, b=20, l=80, r=40),
    )

    return html.Div([
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(figure=month_conv_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=6),
            dbc.Col(html.Div(dcc.Graph(figure=month_vol_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=6),
        ], className='mb-2'),

        html.Div([
            dcc.Graph(figure=dim_conv_fig, config={'displayModeBar': False}),
            dcc.Graph(figure=dim_count_fig, config={'displayModeBar': False}),
        ], className='card-dark mb-2'),

        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(figure=contact_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=6),
            dbc.Col(html.Div(dcc.Graph(figure=pout_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=6),
        ]),
    ])
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/pages/campaign.py
git commit -m "feat: add Campaign Optimization page (Tab 3)"
```

---

## Task 8: Model Performance Page (Tab 4)

**Files:**
- Create: `dashboard/pages/model.py`

- [ ] **Step 1: Create `dashboard/pages/model.py`**

```python
"""Model Performance tab — metrics table, ROC curves, confusion matrix, feature importance."""
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.metrics import roc_curve, confusion_matrix

from dashboard.data_loader import model_metrics, predictions, feature_importance


def layout(filtered_df):
    """Build model performance tab layout. Filters don't apply here — uses full test set."""

    y_test = predictions['y_test']

    # Model comparison table
    table_header = [html.Thead(html.Tr([
        html.Th('Model'), html.Th('Accuracy'), html.Th('Precision'),
        html.Th('Recall'), html.Th('F1'), html.Th('ROC-AUC'),
    ]))]
    rows = []
    for name, m in model_metrics.items():
        is_realistic = 'no duration' in name
        style = {'backgroundColor': '#0f3460'} if is_realistic else {}
        rows.append(html.Tr([
            html.Td(name, style={'fontWeight': 'bold'} if is_realistic else {}),
            html.Td(f"{m['accuracy']:.3f}"),
            html.Td(f"{m['precision']:.3f}"),
            html.Td(f"{m['recall']:.3f}"),
            html.Td(f"{m['f1']:.3f}"),
            html.Td(f"{m['roc_auc']:.3f}"),
        ], style=style))
    table_body = [html.Tbody(rows)]
    metrics_table = dbc.Table(
        table_header + table_body,
        bordered=True, dark=True, hover=True, striped=False,
        style={'fontSize': '14px'},
    )

    # ROC curves — side by side
    roc_fig = make_subplots(rows=1, cols=2,
                            subplot_titles=['With Duration (Unrealistic)', 'Without Duration (Realistic)'])

    model_cols = {
        'LR (with duration)': ('y_prob_lr_wd', 1),
        'DT (with duration)': ('y_prob_dt_wd', 1),
        'LR (no duration)': ('y_prob_lr_nd', 2),
        'DT (no duration)': ('y_prob_dt_nd', 2),
    }
    colors = {'LR': '#3498db', 'DT': '#e74c3c'}

    for name, (col, subplot_col) in model_cols.items():
        fpr, tpr, _ = roc_curve(y_test, predictions[col])
        auc = model_metrics[name]['roc_auc']
        color = colors['LR'] if 'LR' in name else colors['DT']
        roc_fig.add_trace(go.Scatter(
            x=fpr, y=tpr, name=f'{name} (AUC={auc:.3f})',
            line=dict(color=color, width=2),
        ), row=1, col=subplot_col)

    # Random baseline
    for col in [1, 2]:
        roc_fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], name='Random', line=dict(dash='dash', color='gray'),
            showlegend=(col == 1),
        ), row=1, col=col)

    roc_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        height=400, margin=dict(t=40, b=20, l=40, r=20),
    )
    roc_fig.update_xaxes(title_text='False Positive Rate')
    roc_fig.update_yaxes(title_text='True Positive Rate')

    # Confusion matrix — LR no duration (realistic)
    y_pred = predictions['y_pred_lr_nd']
    cm = confusion_matrix(y_test, y_pred)
    cm_fig = go.Figure(go.Heatmap(
        z=cm, x=['Predicted No', 'Predicted Yes'], y=['Actual No', 'Actual Yes'],
        text=cm, texttemplate='%{text}', colorscale='Blues',
    ))
    cm_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        title='Confusion Matrix — LR (Realistic Model)',
        height=350, margin=dict(t=40, b=20, l=80, r=20),
    )

    # Feature importance — top 15
    top15 = feature_importance.head(15).sort_values('importance')
    fi_fig = go.Figure(go.Bar(
        x=top15['importance'], y=top15['feature'], orientation='h',
        marker_color='steelblue',
    ))
    fi_fig.update_layout(
        template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
        title='Top 15 Feature Importances (LR — No Duration)',
        xaxis_title='Absolute Coefficient', height=400,
        margin=dict(t=40, b=20, l=200, r=20),
    )

    return html.Div([
        html.Div([
            html.H5('Model Comparison', style={'color': '#fff', 'marginBottom': '10px'}),
            html.P('Highlighted rows = realistic models (no duration)', style={'color': '#888', 'fontSize': '12px'}),
            metrics_table,
        ], className='card-dark mb-3'),

        html.Div([
            html.P('[NOTE] Models WITH duration perform better due to data leakage — '
                   'duration is only known after the call.',
                   style={'color': '#f39c12', 'fontSize': '13px', 'marginBottom': '5px'}),
            dcc.Graph(figure=roc_fig, config={'displayModeBar': False}),
        ], className='card-dark mb-3'),

        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(figure=cm_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=5),
            dbc.Col(html.Div(dcc.Graph(figure=fi_fig, config={'displayModeBar': False}),
                    className='card-dark'), width=7),
        ]),
    ])
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/pages/model.py
git commit -m "feat: add Model Performance page (Tab 4)"
```

---

## Task 9: ROI Analysis Page (Tab 5 — Star Feature)

**Files:**
- Create: `dashboard/pages/roi.py`

- [ ] **Step 1: Create `dashboard/pages/roi.py`**

```python
"""ROI Analysis tab — threshold slider, real-time ROI calculator, recommendations."""
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from dashboard.data_loader import predictions, COST_PER_CALL, REVENUE_PER_CONVERSION


def layout(filtered_df):
    """Build ROI analysis tab layout with threshold slider."""

    return html.Div([
        html.Div([
            html.H5('ROI Threshold Simulator', style={'color': '#fff'}),
            html.P('Drag the slider to see how different probability thresholds affect ROI.',
                   style={'color': '#888', 'fontSize': '13px'}),
            dcc.Slider(
                id='roi-threshold-slider',
                min=0.1, max=0.9, step=0.05, value=0.3,
                marks={i/10: f'{i/10:.1f}' for i in range(1, 10)},
                tooltip={'placement': 'bottom', 'always_visible': True},
            ),
        ], className='card-dark mb-3'),

        # Dynamic KPI cards for ROI
        html.Div(id='roi-kpi-cards'),

        # Dynamic comparison chart
        html.Div(id='roi-comparison-chart', className='card-dark mb-3'),

        # Dynamic savings text
        html.Div(id='roi-savings-text', className='card-dark mb-3'),

        # Strategy comparison table (static)
        html.Div(id='roi-strategy-table', className='card-dark mb-3'),

        # Recommendations
        html.H5('5 Actionable Recommendations', style={'color': '#fff', 'marginTop': '20px'}),
        html.Div([
            html.Div([
                html.Strong('1. Target High-Value Segments'),
                html.P('Focus calls on customer segments with highest conversion rates. Stop blanket calling.'),
            ], className='recommendation-card'),
            html.Div([
                html.Strong('2. Use the Predictive Model for Call Lists'),
                html.P('Our model identifies high-probability subscribers. Use it to build targeted call lists.'),
            ], className='recommendation-card'),
            html.Div([
                html.Strong('3. Limit Calls to 3 Per Customer'),
                html.P('Conversion rate drops sharply after 3 calls. Additional calls waste money.'),
            ], className='recommendation-card'),
            html.Div([
                html.Strong('4. Prioritize Cellular Contact & Best Months'),
                html.P('Cellular contacts convert better. Focus campaign intensity on high-conversion months.'),
            ], className='recommendation-card'),
            html.Div([
                html.Strong('5. Leverage Previous Campaign Success'),
                html.P('Customers who converted before are far more likely to convert again. Call them first.'),
            ], className='recommendation-card'),
        ]),
    ])


def register_callbacks(app):
    """Register ROI slider callbacks."""

    @app.callback(
        [Output('roi-kpi-cards', 'children'),
         Output('roi-comparison-chart', 'children'),
         Output('roi-savings-text', 'children'),
         Output('roi-strategy-table', 'children')],
        [Input('roi-threshold-slider', 'value')],
    )
    def update_roi(threshold):
        y_test = predictions['y_test']
        y_prob = predictions['y_prob_lr_nd']

        # Current strategy (call everyone)
        total = len(y_test)
        total_conv = int(y_test.sum())
        current_cost = total * COST_PER_CALL
        current_rev = total_conv * REVENUE_PER_CONVERSION
        current_profit = current_rev - current_cost
        current_roi = (current_rev - current_cost) / current_cost * 100

        # Targeted strategy
        mask = y_prob >= threshold
        t_calls = int(mask.sum())
        t_conv = int(y_test[mask].sum())
        t_cost = t_calls * COST_PER_CALL
        t_rev = t_conv * REVENUE_PER_CONVERSION
        t_profit = t_rev - t_cost
        t_roi = (t_rev - t_cost) / t_cost * 100 if t_cost > 0 else 0

        calls_saved = (1 - t_calls / total) * 100
        conv_retained = t_conv / total_conv * 100 if total_conv > 0 else 0

        # KPI cards
        kpi_cards = dbc.Row([
            dbc.Col(html.Div([
                html.Div(f'{t_calls:,}', className='kpi-value', style={'color': '#2ecc71'}),
                html.Div('Targeted Calls', className='kpi-label'),
            ], className='kpi-card'), width=2),
            dbc.Col(html.Div([
                html.Div(f'{t_conv:,}', className='kpi-value', style={'color': '#3498db'}),
                html.Div('Conversions', className='kpi-label'),
            ], className='kpi-card'), width=2),
            dbc.Col(html.Div([
                html.Div(f'EUR {t_cost:,.0f}', className='kpi-value', style={'color': '#e74c3c'}),
                html.Div('Cost', className='kpi-label'),
            ], className='kpi-card'), width=2),
            dbc.Col(html.Div([
                html.Div(f'EUR {t_rev:,.0f}', className='kpi-value', style={'color': '#2ecc71'}),
                html.Div('Revenue', className='kpi-label'),
            ], className='kpi-card'), width=2),
            dbc.Col(html.Div([
                html.Div(f'EUR {t_profit:,.0f}', className='kpi-value', style={'color': '#f39c12'}),
                html.Div('Profit', className='kpi-label'),
            ], className='kpi-card'), width=2),
            dbc.Col(html.Div([
                html.Div(f'{t_roi:.0f}%', className='kpi-value', style={'color': '#9b59b6'}),
                html.Div('ROI', className='kpi-label'),
            ], className='kpi-card'), width=2),
        ], className='mb-3')

        # Comparison bar chart
        comp_fig = go.Figure()
        metrics_names = ['Calls', 'Cost (EUR)', 'Conversions', 'ROI (%)']
        current_vals = [total, current_cost, total_conv, current_roi]
        targeted_vals = [t_calls, t_cost, t_conv, t_roi]

        from plotly.subplots import make_subplots
        comp_fig = make_subplots(rows=1, cols=4, subplot_titles=metrics_names)
        for i, (name, cv, tv) in enumerate(zip(metrics_names, current_vals, targeted_vals)):
            comp_fig.add_trace(go.Bar(x=['Current', 'Targeted'], y=[cv, tv],
                              marker_color=['#e74c3c', '#2ecc71'], showlegend=False),
                              row=1, col=i+1)
        comp_fig.update_layout(
            template='plotly_dark', paper_bgcolor='#16213e', plot_bgcolor='#16213e',
            height=300, margin=dict(t=40, b=20, l=40, r=20),
            title_text='Current vs Targeted Strategy',
        )

        # Savings text
        savings_text = html.Div([
            html.H4(f'You save {calls_saved:.0f}% of calls while retaining {conv_retained:.0f}% of conversions.',
                    style={'color': '#2ecc71', 'textAlign': 'center'}),
            html.P(f'Cost savings: EUR {current_cost - t_cost:,.0f} | '
                   f'ROI improvement: {current_roi:.0f}% -> {t_roi:.0f}%',
                   style={'color': '#888', 'textAlign': 'center'}),
        ])

        # Strategy table — multiple thresholds
        thresholds = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        table_rows = []
        for t in thresholds:
            m = y_prob >= t
            tc = int(m.sum())
            tconv = int(y_test[m].sum())
            tcost = tc * COST_PER_CALL
            trev = tconv * REVENUE_PER_CONVERSION
            troi = (trev - tcost) / tcost * 100 if tcost > 0 else 0
            is_selected = abs(t - threshold) < 0.01
            style = {'backgroundColor': '#0f3460', 'fontWeight': 'bold'} if is_selected else {}
            table_rows.append(html.Tr([
                html.Td(f'{t:.1f}'), html.Td(f'{tc:,}'),
                html.Td(f'{tconv:,}'), html.Td(f'EUR {tcost:,.0f}'),
                html.Td(f'{troi:.0f}%'),
            ], style=style))

        strategy_table = html.Div([
            html.H6('All Thresholds Comparison', style={'color': '#fff', 'marginBottom': '10px'}),
            dbc.Table([
                html.Thead(html.Tr([
                    html.Th('Threshold'), html.Th('Calls'), html.Th('Conversions'),
                    html.Th('Cost'), html.Th('ROI'),
                ])),
                html.Tbody(table_rows),
            ], bordered=True, dark=True, hover=True, size='sm'),
        ])

        return kpi_cards, dcc.Graph(figure=comp_fig, config={'displayModeBar': False}), savings_text, strategy_table
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/pages/roi.py
git commit -m "feat: add ROI Analysis page with threshold slider (Tab 5)"
```

---

## Task 10: Main App (app.py)

**Files:**
- Create: `dashboard/app.py`

- [ ] **Step 1: Create `dashboard/app.py`**

```python
"""Main Dash application — layout, tabs, global callbacks."""
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

from dashboard.data_loader import df, filter_dataframe, predictions, COST_PER_CALL, REVENUE_PER_CONVERSION
from dashboard.components.kpi_cards import kpi_row, empty_kpi_row
from dashboard.components.filters import filter_bar
from dashboard.pages import overview, segments, campaign, model, roi

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title='Bank Marketing ROI Dashboard',
)
server = app.server  # For Gunicorn deployment

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        dbc.Row([
            dbc.Col(
                html.H4('Bank Marketing ROI Dashboard',
                        style={'color': '#e94560', 'fontWeight': 'bold', 'margin': '0'}),
                width='auto',
            ),
            dbc.Col(
                dbc.Tabs(
                    id='main-tabs',
                    active_tab='overview',
                    children=[
                        dbc.Tab(label='Overview', tab_id='overview'),
                        dbc.Tab(label='Segments', tab_id='segments'),
                        dbc.Tab(label='Campaign', tab_id='campaign'),
                        dbc.Tab(label='Model', tab_id='model'),
                        dbc.Tab(label='ROI', tab_id='roi'),
                    ],
                ),
            ),
        ], align='center', className='mb-3'),
    ], style={'padding': '16px 20px 0'}),

    # Filter bar
    html.Div([filter_bar()], style={'padding': '0 20px'}),

    # KPI cards
    html.Div(id='kpi-cards-container', style={'padding': '0 20px'}),

    # Tab content
    html.Div(id='tab-content', style={'padding': '0 20px 20px'}),

], style={'backgroundColor': '#1a1a2e', 'minHeight': '100vh'})

# Register page-specific callbacks
roi.register_callbacks(app)
segments.register_callbacks(app)


@callback(
    [Output('kpi-cards-container', 'children'),
     Output('tab-content', 'children')],
    [Input('main-tabs', 'active_tab'),
     Input('filter-job', 'value'),
     Input('filter-age', 'value'),
     Input('filter-education', 'value')],
)
def update_tab(active_tab, job, age, education):
    """Update KPI cards and tab content based on active tab and filters."""
    filtered = filter_dataframe(job, age, education)

    if filtered.empty:
        return empty_kpi_row(), html.Div(
            "No data for selected filters.", className='card-dark',
            style={'textAlign': 'center', 'padding': '40px'})

    # KPI values
    total = len(filtered)
    conv_rate = filtered['y_numeric'].mean() * 100

    # Targeted ROI and Cost Savings are computed from full predictions
    # (not filtered — model predictions don't have demographic columns)
    y_prob = predictions['y_prob_lr_nd']
    y_test = predictions['y_test']
    mask = y_prob >= 0.3
    t_cost = int(mask.sum()) * COST_PER_CALL
    t_rev = int(y_test[mask].sum()) * REVENUE_PER_CONVERSION
    targeted_roi = (t_rev - t_cost) / t_cost * 100 if t_cost > 0 else 0
    cost_savings = (1 - int(mask.sum()) / len(y_test)) * 100

    kpi = kpi_row(total, conv_rate, targeted_roi, cost_savings)

    # Render active tab
    tab_map = {
        'overview': overview.layout,
        'segments': segments.layout,
        'campaign': campaign.layout,
        'model': model.layout,
        'roi': roi.layout,
    }
    content = tab_map.get(active_tab, overview.layout)(filtered)

    return kpi, content


@callback(
    [Output('filter-job', 'value'),
     Output('filter-age', 'value'),
     Output('filter-education', 'value')],
    [Input('reset-filters', 'n_clicks')],
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    """Reset all filters to 'All'."""
    return 'All', 'All', 'All'


if __name__ == '__main__':
    app.run(debug=True, port=8050)
```

- [ ] **Step 2: Test the app locally**

Run: `cd "C:/Users/agran/agks/marketanalysis" && python -m dashboard.app`
Expected: Server starts at http://localhost:8050. Open in browser to verify all 5 tabs work.

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/app.py
git commit -m "feat: add main Dash app with tabs, filters, and global callbacks"
```

---

## Task 11: Local Testing & Bug Fixes

- [ ] **Step 1: Run the full dashboard**

Run: `cd "C:/Users/agran/agks/marketanalysis" && python -m dashboard.app`
Open http://localhost:8050 in the browser.

- [ ] **Step 2: Test each tab**

Verify:
- Overview: pie chart, job bar chart, key findings display
- Segments: segment bar charts, top/bottom segments, persona card
- Campaign: monthly charts, diminishing returns, contact + poutcome charts
- Model: metrics table, ROC curves, confusion matrix, feature importance
- ROI: threshold slider updates all KPIs, chart, savings text, and table in real-time

- [ ] **Step 3: Test filters**

- Select "management" in Job filter — all charts on active tab should update
- Select "18-30" in Age — charts update
- Click "Reset Filters" — everything resets to All
- Switch tabs — content updates with current filter values

- [ ] **Step 4: Fix any bugs found**

Address any import errors, missing data columns, or layout issues.

- [ ] **Step 5: Commit fixes**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add dashboard/
git commit -m "fix: address dashboard bugs from local testing"
```

---

## Task 12: Deploy to Render

- [ ] **Step 1: Push all changes to GitHub**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git push origin master
```

- [ ] **Step 2: Update README with dashboard link**

Add a "Live Dashboard" section to README.md with the Render URL (to be filled after deployment).

- [ ] **Step 3: Deploy on Render**

Go to https://render.com:
1. Sign up / log in with GitHub
2. Click "New" → "Web Service"
3. Connect your `agrani1411/marketanalysis` repo
4. Settings:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn dashboard.app:server`
   - Environment: Python 3
5. Click "Create Web Service"

If Render free tier is unavailable, use Railway or Hugging Face Spaces as fallback.

- [ ] **Step 4: Verify deployment**

Open the Render URL. Verify all 5 tabs work and the threshold slider is interactive.

- [ ] **Step 5: Update README and blog post with live URL**

```bash
cd "C:/Users/agran/agks/marketanalysis"
git add README.md blog_post.md
git commit -m "docs: add live dashboard URL to README and blog post"
git push origin master
```

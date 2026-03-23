"""Load all data files once at startup."""
import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'cleaned')

df = pd.read_csv(os.path.join(DATA_DIR, 'bank-cleaned.csv'))
predictions = pd.read_csv(os.path.join(DATA_DIR, 'model-predictions.csv'))

with open(os.path.join(DATA_DIR, 'model-metrics.json'), 'r') as f:
    model_metrics = json.load(f)

feature_importance = pd.read_csv(os.path.join(DATA_DIR, 'feature-importance.csv'))

COST_PER_CALL = 5
REVENUE_PER_CONVERSION = 200

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
    filtered = df.copy()
    if job != 'All':
        filtered = filtered[filtered['job'] == job]
    if age != 'All':
        filtered = filtered[filtered['age_group'] == age]
    if education != 'All':
        filtered = filtered[filtered['education'] == education]
    return filtered

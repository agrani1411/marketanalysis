"""Global filter bar component."""
from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard.data_loader import JOB_OPTIONS, AGE_OPTIONS, EDUCATION_OPTIONS


def filter_bar():
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

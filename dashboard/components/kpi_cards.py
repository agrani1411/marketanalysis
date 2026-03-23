"""Reusable KPI card row component."""
from dash import html
import dash_bootstrap_components as dbc


def make_kpi_card(title, value, color):
    return dbc.Col(
        html.Div([
            html.Div(value, className='kpi-value', style={'color': color}),
            html.Div(title, className='kpi-label'),
        ], className='kpi-card'),
        width=3,
    )


def kpi_row(total_customers, conversion_rate, targeted_roi, cost_savings):
    return dbc.Row([
        make_kpi_card('Total Customers', f'{total_customers:,}', '#2ecc71'),
        make_kpi_card('Conversion Rate', f'{conversion_rate:.1f}%', '#e74c3c'),
        make_kpi_card('Targeted ROI', f'{targeted_roi:.0f}%', '#3498db'),
        make_kpi_card('Cost Savings', f'{cost_savings:.0f}%', '#f39c12'),
    ], className='mb-3')


def empty_kpi_row():
    return dbc.Row([
        make_kpi_card('Total Customers', '-', '#888'),
        make_kpi_card('Conversion Rate', '-', '#888'),
        make_kpi_card('Targeted ROI', '-', '#888'),
        make_kpi_card('Cost Savings', '-', '#888'),
    ], className='mb-3')

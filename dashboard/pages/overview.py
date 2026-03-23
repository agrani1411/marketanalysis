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

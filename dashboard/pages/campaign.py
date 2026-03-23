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

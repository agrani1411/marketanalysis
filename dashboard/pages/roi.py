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

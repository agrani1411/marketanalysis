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

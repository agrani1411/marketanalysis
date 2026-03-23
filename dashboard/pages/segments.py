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

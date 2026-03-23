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

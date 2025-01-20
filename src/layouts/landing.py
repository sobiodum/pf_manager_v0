"""
Landing page layout for the Portfolio Analysis Tool.
File: src/layouts/landing.py
"""

from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src="/assets/logo-large.png", className="mb-4"),
                html.H1("Portfolio Analysis Tool", className="display-4 mb-4"),
                html.P(
                    "Professional portfolio management and analysis with Bloomberg integration",
                    className="lead mb-5"
                ),
                
                # Quick access buttons
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            [
                                html.I(className="fas fa-plus-circle me-2"),
                                "Create New Portfolio"
                            ],
                            color="primary",
                            size="lg",
                            id={'type': 'landing-button', 'page': 'portfolio-builder'},
                            n_clicks=0,
                            className="me-3"
                        ),
                    ], width="auto"),
                    dbc.Col([
                        dbc.Button(
                            [
                                html.I(className="fas fa-chart-line me-2"),
                                "View Active Portfolios"
                            ],
                            color="secondary",
                            size="lg",
                            id={'type': 'landing-button', 'page': 'portfolio-monitor'},
                            n_clicks=0,
                            className="me-3"
                        ),
                    ], width="auto"),
                ], justify="center", className="mt-4"),
            ], className="text-center landing-content")
        ], width=12)
    ])
], fluid=True, className="landing-container")
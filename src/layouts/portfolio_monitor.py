"""
Portfolio monitor layout implementation.
File: src/layouts/portfolio_monitor.py
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

def create_portfolio_summary(portfolio_data):
    """Create the portfolio summary card."""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                # Portfolio name and value
                dbc.Col([
                    html.H3(portfolio_data["name"], className="mb-1"),
                    html.H4(
                        f"${portfolio_data['total_value']:,.2f}", 
                        className="text-primary mb-2"
                    ),
                ], md=6),
                
                # P&L metrics
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div("Today's Change", className="text-muted small"),
                            html.Div([
                                html.I(
                                    className="fas fa-caret-up me-1 text-success" 
                                    if portfolio_data["day_change"] > 0 
                                    else "fas fa-caret-down me-1 text-danger"
                                ),
                                f"{abs(portfolio_data['day_change']):.2f}%"
                            ], className="h5 mb-0"),
                        ]),
                        dbc.Col([
                            html.Div("Total P&L", className="text-muted small"),
                            html.Div([
                                html.I(
                                    className="fas fa-caret-up me-1 text-success"
                                    if portfolio_data["total_pnl"] > 0
                                    else "fas fa-caret-down me-1 text-danger"
                                ),
                                f"${abs(portfolio_data['total_pnl']):,.2f}"
                            ], className="h5 mb-0"),
                        ]),
                    ])
                ], md=6),
            ]),
            
            # Sparkline chart
            dcc.Graph(
                id="portfolio-sparkline",
                figure={
                    "data": [{
                        "x": portfolio_data["history_dates"],
                        "y": portfolio_data["history_values"],
                        "type": "scatter",
                        "mode": "lines",
                        "line": {"color": "#375a7f"},
                    }],
                    "layout": {
                        "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
                        "height": 80,
                        "showlegend": False,
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "xaxis": {"showgrid": False, "zeroline": False, "showticklabels": False},
                        "yaxis": {"showgrid": False, "zeroline": False, "showticklabels": False}
                    }
                },
                config={"displayModeBar": False}
            )
        ])
    ], className="mb-4")

def create_holdings_table(holdings):
    """Create the holdings table."""
    return dbc.Card([
        dbc.CardHeader(html.H5("Holdings", className="mb-0")),
        dbc.CardBody([
            html.Div([
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Instrument"),
                            html.Th("Quantity"),
                            html.Th("Avg Cost"),
                            html.Th("Current Price"),
                            html.Th("Market Value"),
                            html.Th("P&L (Local)"),
                            html.Th("P&L (USD)"),
                            html.Th("P&L %"),
                            html.Th("Weight"),
                            html.Th("Actions")
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            # Instrument details
                            html.Td([
                                html.Div(holding["ticker"], className="fw-bold"),
                                html.Small(holding["name"], className="text-muted d-block")
                            ]),
                            html.Td(f"{holding['quantity']:,.0f}"),
                            html.Td(f"${holding['avg_cost']:.2f}"),
                            html.Td(f"${holding['current_price']:.2f}"),
                            html.Td(f"${holding['market_value']:,.2f}"),
                            
                            # P&L columns
                            html.Td(
                                [
                                    html.I(
                                        className="fas fa-caret-up me-1 text-success"
                                        if holding['pnl_local'] > 0
                                        else "fas fa-caret-down me-1 text-danger"
                                    ),
                                    f"${abs(holding['pnl_local']):,.2f}"
                                ],
                                className="text-success" if holding['pnl_local'] > 0 else "text-danger"
                            ),
                            html.Td(
                                [
                                    html.I(
                                        className="fas fa-caret-up me-1 text-success"
                                        if holding['pnl_usd'] > 0
                                        else "fas fa-caret-down me-1 text-danger"
                                    ),
                                    f"${abs(holding['pnl_usd']):,.2f}"
                                ],
                                className="text-success" if holding['pnl_usd'] > 0 else "text-danger"
                            ),
                            html.Td(
                                f"{holding['pnl_percent']:.2f}%",
                                className="text-success" if holding['pnl_percent'] > 0 else "text-danger"
                            ),
                            
                            # Weight and actions
                            html.Td(f"{holding['weight']:.1f}%"),
                            html.Td([
                                dbc.Button(
                                    html.I(className="fas fa-chevron-down"),
                                    color="link",
                                    size="sm",
                                    id={"type": "expand-trades", "index": holding["ticker"]},
                                )
                            ])
                        ]) for holding in holdings
                    ])
                ], bordered=True, hover=True, responsive=True)
            ], style={"overflowX": "auto"})
        ])
    ], className="mb-4")

def create_allocation_charts():
    """Create allocation analysis charts."""
    return dbc.Card([
        dbc.CardHeader(html.H5("Portfolio Analysis", className="mb-0")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Asset Allocation", className="text-center mb-3"),
                    dcc.Graph(
                        id="asset-allocation-chart",
                        config={"displayModeBar": False}
                    )
                ], md=6),
                dbc.Col([
                    html.H6("Geographic Distribution", className="text-center mb-3"),
                    dcc.Graph(
                        id="geographic-allocation-chart",
                        config={"displayModeBar": False}
                    )
                ], md=6),
            ])
        ])
    ])

# Import required libraries at the top level
import plotly.express as px
import plotly.graph_objects as go

# Main layout
layout = dbc.Container([
    # Header section
    dbc.Row([
        dbc.Col([
            html.H2("Portfolio Monitor", className="mb-4")
        ], width=8),
        dbc.Col([
            dbc.Button(
                [html.I(className="fas fa-sync-alt me-2"), "Refresh Data"],
                color="primary",
                id="refresh-data-btn",
                className="float-end"
            )
        ], width=4)
    ], className="mb-4"),
    
    # Portfolio selector
    dbc.Row([
        dbc.Col([
            dbc.Select(
                id="portfolio-selector",
                options=[
                    {"label": "Growth Portfolio", "value": "growth"},
                    {"label": "Income Portfolio", "value": "income"},
                    {"label": "Balanced Portfolio", "value": "balanced"}
                ],
                value="growth",
                className="mb-4"
            )
        ])
    ]),
    
    # Hidden stores for state management
    dcc.Store(id="portfolio-data", data={}),
    dcc.Store(id="holdings-data", data=[]),
    
    # Main content area with portfolio summary, holdings, and analysis
    html.Div(id="monitor-content")
], fluid=True)
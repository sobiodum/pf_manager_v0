"""
Portfolio builder layout for instrument search and portfolio creation.
File: src/layouts/portfolio_builder.py
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_search_section():
    """Create the instrument search section."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("Search Instruments", className="mb-0")
        ]),
        dbc.CardBody([
            # Search input
            dbc.InputGroup([
                dbc.Input(
                    id="search-input",
                    type="text",
                    placeholder="Enter ticker or company name...",
                    debounce=True
                ),
                dbc.InputGroupText(
                    html.I(className="fas fa-search")
                )
            ], className="mb-3"),
            
            # Search results area
            html.Div(id="search-results", style={"maxHeight": "300px", "overflowY": "auto"}),
            
            # Selected instruments display with weights
            html.Div([
                html.H6("Selected Instruments", className="mt-4 mb-3"),
                html.Div(id="selected-instruments-display"),
                
                # Portfolio weights summary
                dbc.Alert(
                    [
                        html.I(className="fas fa-info-circle me-2"),
                        "Total allocation: ",
                        html.Span(id="total-allocation", className="fw-bold")
                    ],
                    id="allocation-alert",
                    color="primary",
                    className="mt-3"
                ),
                
                # Warning for invalid allocation
                dbc.Alert(
                    [
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "Total allocation must equal 100%"
                    ],
                    id="allocation-warning",
                    color="warning",
                    is_open=False,
                    className="mt-2"
                )
            ])
        ])
    ], className="mb-4")

def create_portfolio_config():
    """Create the portfolio configuration section."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("Portfolio Configuration", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Base Currency"),
                    dcc.Dropdown(
                        id="base-currency",
                        options=[
                            {"label": "USD", "value": "USD"},
                            {"label": "EUR", "value": "EUR"},
                            {"label": "CHF", "value": "CHF"}
                        ],
                        value="USD",
                        className="mb-3"
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Time Range"),
                    dcc.Dropdown(
                        id="time-range",
                        options=[
                            {"label": "6 Months", "value": "6M"},
                            {"label": "1 Year", "value": "1Y"},
                            {"label": "2 Years", "value": "2Y"},
                            {"label": "3 Years", "value": "3Y"},
                            {"label": "4 Years", "value": "4Y"},
                            {"label": "5 Years", "value": "5Y"},
                            {"label": "Maximum", "value": "max"}
                        ],
                        value="1Y",
                        className="mb-3"
                    )
                ], md=6)
            ])
        ])
    ], className="mb-4")

def create_metrics_section():
    """Create the portfolio metrics section."""
    return dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col(html.H5("Portfolio Analysis", className="mb-0"), width=8),
                dbc.Col(
                    dbc.Button(
                        [html.I(className="fas fa-chart-line me-2"), "Generate Portfolio"],
                        id="generate-portfolio-btn",
                        color="success",
                        className="float-end",
                        n_clicks=0
                    ),
                    width=4
                )
            ])
        ]),
        dbc.CardBody([
            # Status message for data loading
            html.Div(id="portfolio-status-message", className="mb-3"),
            
            # Performance chart
            dcc.Graph(
                id="performance-chart",
                config={'displayModeBar': True},
                className="mb-4"
            ),
            
            # Metrics table
            html.Div(id="metrics-table")
        ])
    ])

# Main layout
layout = dbc.Container([
    # Hidden stores for state management
    dcc.Store(id="selected-instruments", data=[]),
    
    # Header section
    dbc.Row([
        dbc.Col([
            html.H2("Portfolio Builder", className="mb-4"),
            html.P("Create and analyze your portfolio by searching for instruments and setting allocations.")
        ])
    ], className="mb-4"),
    
    # Main content
    dbc.Row([
        # Left column - Search and Configuration
        dbc.Col([
            create_search_section(),
            create_portfolio_config()
        ], lg=5),
        
        # Right column - Charts and Metrics
        dbc.Col([
            create_metrics_section()
        ], lg=7)
    ])
], fluid=True)
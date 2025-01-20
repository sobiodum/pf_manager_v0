"""
Portfolio monitor layout.
File: src/layouts/portfolio_monitor.py
"""

from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H2("Portfolio Monitor", className="mb-4"),
    html.P("Portfolio monitoring interface will be implemented here.")
], fluid=True)
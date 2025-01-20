"""
Portfolio builder layout.
File: src/layouts/portfolio_builder.py
"""

from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H2("Portfolio Builder", className="mb-4"),
    html.P("Portfolio builder interface will be implemented here.")
], fluid=True)
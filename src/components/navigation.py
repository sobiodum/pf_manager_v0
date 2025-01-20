"""
Navigation sidebar component for the Portfolio Analysis Tool.
File: src/components/navigation.py
"""

from dash import html
import dash_bootstrap_components as dbc

def create_navigation():
    """Create the navigation sidebar."""
    return html.Div([
        dbc.Nav([
            dbc.NavLink(
                [html.I(className="fas fa-home me-2"), "Home"],
                href="#",
                id="nav-home",
                className="nav-link",
                active="exact"
            ),
            dbc.NavLink(
                [html.I(className="fas fa-plus-circle me-2"), "Portfolio Builder"],
                href="#",
                id="nav-portfolio-builder",
                className="nav-link"
            ),
            dbc.NavLink(
                [html.I(className="fas fa-chart-line me-2"), "Portfolio Monitor"],
                href="#",
                id="nav-portfolio-monitor",
                className="nav-link"
            ),
        ],
        vertical=True,
        pills=True,
        className="flex-column nav-pills"
        )
    ], className="nav-sidebar bg-dark")
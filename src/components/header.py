"""
Header component containing Bloomberg status and corporate branding.
File: src/components/header.py
"""

from dash import html
import dash_bootstrap_components as dbc
from components.bloomberg_status import create_bloomberg_status

def create_header():
    """Create the application header."""
    return dbc.Navbar(
        dbc.Container([
            # Corporate Logo
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                    dbc.Col(dbc.NavbarBrand("Portfolio Analysis Tool", className="ms-2")),
                ],
                align="center",
                className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            
            # Bloomberg Status and Timestamp
            dbc.Row([
                dbc.Col(create_bloomberg_status(), className="me-3"),
                dbc.Col(
                    html.Div([
                        html.Small("Last Update: ", className="text-muted"),
                        html.Small(id="last-update-time", className="text-light"),
                    ]),
                    className="text-end"
                ),
            ]),
        ],
        fluid=True
        ),
        color="dark",
        dark=True,
        className="mb-4",
    )
"""
Bloomberg connection status indicator component.
File: src/components/bloomberg_status.py
"""

from dash import html
import dash_bootstrap_components as dbc

def create_bloomberg_status():
    """Create Bloomberg connection status indicator."""
    return html.Div([
        html.Span(
            className="status-indicator status-disconnected",
            id="bloomberg-status-indicator"
        ),
        html.Span(
            "Bloomberg: Disconnected",
            id="bloomberg-status-text",
            className="text-muted"
        )
    ], className="bloomberg-status")

# TODO: Add callback to update status when Bloomberg connection is implemented
def init_bloomberg_status_callbacks(app):
    """Initialize Bloomberg status callbacks."""
    pass  # Will be implemented when Bloomberg connection is added
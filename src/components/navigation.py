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

# Navigation callback
def init_navigation_callbacks(app):
    """Initialize navigation callbacks."""
    @app.callback(
        dash.Output('current-page', 'data'),
        [
            dash.Input('nav-home', 'n_clicks'),
            dash.Input('nav-portfolio-builder', 'n_clicks'),
            dash.Input('nav-portfolio-monitor', 'n_clicks')
        ]
    )
    def navigate(home_clicks, builder_clicks, monitor_clicks):
        """Handle navigation between pages."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return 'landing'
            
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'nav-portfolio-builder':
            return 'portfolio-builder'
        elif button_id == 'nav-portfolio-monitor':
            return 'portfolio-monitor'
        else:
            return 'landing'
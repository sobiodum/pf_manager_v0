"""
Main application entry point for the Portfolio Analysis Tool.
File: src/app.py
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts import landing, portfolio_builder, portfolio_monitor
from components.header import create_header
from components.navigation import create_navigation

# Initialize the Dash app with dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

# Main app layout
app.layout = html.Div([
    # Store for current page
    dcc.Store(id='current-page', data='landing'),
    
    # Header
    create_header(),
    
    # Main content area with navigation and page content
    dbc.Container([
        dbc.Row([
            # Navigation sidebar
            dbc.Col(create_navigation(), width=2, className='nav-sidebar'),
            
            # Main content area
            dbc.Col([
                html.Div(id='page-content', className='content-container')
            ], width=10)
        ])
    ], fluid=True, className='main-container')
])

# Callback for page routing
@app.callback(
    dash.Output('page-content', 'children'),
    [dash.Input('current-page', 'data')]
)
def display_page(page):
    """Route to the appropriate page based on the current-page store value."""
    if page == 'portfolio-builder':
        return portfolio_builder.layout
    elif page == 'portfolio-monitor':
        return portfolio_monitor.layout
    else:  # Default to landing page
        return landing.layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
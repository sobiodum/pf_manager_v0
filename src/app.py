

"""
Main application entry point for the Portfolio Analysis Tool.
File: src/app.py
"""

import dash
from dash import html, dcc, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from layouts import landing, portfolio_builder, portfolio_monitor
from components.header import create_header
from components.navigation import create_navigation
from callbacks.portfolio_builder_callbacks import init_portfolio_builder_callbacks
from callbacks.portfolio_monitor_callbacks import init_portfolio_monitor_callbacks

print("Starting Portfolio Analysis Tool...")  # Debug log

# Initialize the Dash app with dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ],
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

print("App layout created")  # Debug log

# Sidebar navigation callback
@app.callback(
    Output('current-page', 'data'),
    [Input('nav-home', 'n_clicks'),
     Input('nav-portfolio-builder', 'n_clicks'),
     Input('nav-portfolio-monitor', 'n_clicks')],
    State('current-page', 'data')
)
def handle_navigation(home_clicks, builder_clicks, monitor_clicks, current):
    """Handle navigation from sidebar."""
    print("Navigation callback triggered")  # Debug log
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return current
        
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"Navigation to: {button_id}")  # Debug log
    
    # Map button IDs to pages
    page_mapping = {
        'nav-home': 'landing',
        'nav-portfolio-builder': 'portfolio-builder',
        'nav-portfolio-monitor': 'portfolio-monitor'
    }
    
    return page_mapping.get(button_id, current)

# Page content callback
@app.callback(
    Output('page-content', 'children'),
    [Input('current-page', 'data')]
)
def display_page(page):
    """Route to the appropriate page based on the current-page store value."""
    print(f"Displaying page: {page}")  # Debug log
    
    if page == 'portfolio-builder':
        return portfolio_builder.layout
    elif page == 'portfolio-monitor':
        return portfolio_monitor.layout
    else:  # Default to landing page
        return landing.layout

# Landing page button callback
@app.callback(
    Output('current-page', 'data', allow_duplicate=True),
    [Input({'type': 'landing-button', 'page': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def handle_landing_buttons(n_clicks):
    """Handle clicks from landing page buttons."""
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
        
    triggered_id = ctx.triggered[0]['prop_id']
    print(f"Landing button clicked: {triggered_id}")  # Debug log
    
    if 'page":"portfolio-builder"' in triggered_id:
        return 'portfolio-builder'
    elif 'page":"portfolio-monitor"' in triggered_id:
        return 'portfolio-monitor'
    
    raise dash.exceptions.PreventUpdate

print("Initializing callbacks...")  # Debug log

# Initialize all callbacks
init_portfolio_builder_callbacks(app)
init_portfolio_monitor_callbacks(app)

print("All callbacks initialized")  # Debug log

# Run the app
if __name__ == '__main__':
    print("Starting server...")  # Debug log
    app.run_server(debug=True)
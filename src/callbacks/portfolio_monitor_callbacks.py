"""
Callbacks for the Portfolio Monitor view.
File: src/callbacks/portfolio_monitor_callbacks.py
"""

from dash import html, Input, Output, State, callback_context
from layouts.portfolio_monitor import create_portfolio_summary, create_holdings_table, create_allocation_charts
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

def generate_mock_portfolio_data(portfolio_id):
    """Generate mock portfolio data for development."""
    print(f"Generating mock data for portfolio: {portfolio_id}")  # Debug log
    
    # Generate mock historical data
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') 
            for x in range(30, 0, -1)]
    base_value = 1000000
    values = [base_value * (1 + np.random.normal(0, 0.02)) 
             for _ in range(len(dates))]
    
    portfolio_data = {
        "id": portfolio_id,
        "name": f"{portfolio_id.title()} Portfolio",
        "total_value": values[-1],
        "day_change": ((values[-1] / values[-2]) - 1) * 100,
        "total_pnl": values[-1] - base_value,
        "history_dates": dates,
        "history_values": values
    }
    
    print(f"Generated portfolio data: {portfolio_data['name']}")  # Debug log
    return portfolio_data

def generate_mock_holdings():
    """Generate mock holdings data for development."""
    print("Generating mock holdings data")  # Debug log
    
    holdings = [
        {
            "ticker": "AAPL US Equity",
            "name": "Apple Inc",
            "quantity": 1000,
            "avg_cost": 150.00,
            "current_price": 175.50,
            "market_value": 175500.00,
            "pnl_local": 25500.00,
            "pnl_usd": 25500.00,
            "pnl_percent": 17.00,
            "weight": 15.5,
            "sector": "Technology",
            "region": "North America"
        },
        {
            "ticker": "MSFT US Equity",
            "name": "Microsoft Corp",
            "quantity": 800,
            "avg_cost": 200.00,
            "current_price": 235.75,
            "market_value": 188600.00,
            "pnl_local": 28600.00,
            "pnl_usd": 28600.00,
            "pnl_percent": 14.30,
            "weight": 16.8,
            "sector": "Technology",
            "region": "North America"
        }
    ]
    
    print(f"Generated {len(holdings)} holdings")  # Debug log
    return holdings

def init_portfolio_monitor_callbacks(app):
    """Initialize callbacks for the portfolio monitor view."""
    print("Initializing portfolio monitor callbacks...")  # Debug log
    
    @app.callback(
        [Output("portfolio-data", "data"),
         Output("holdings-data", "data")],
        [Input("portfolio-selector", "value"),
         Input("refresh-data-btn", "n_clicks")]
    )
    def update_portfolio_data(portfolio_id, n_clicks):
        """Update portfolio and holdings data."""
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
        print(f"update_portfolio_data triggered by: {triggered}")  # Debug log
        print(f"Portfolio ID: {portfolio_id}, n_clicks: {n_clicks}")  # Debug log
        
        if not portfolio_id:
            print("No portfolio_id provided")  # Debug log
            return {}, []
            
        portfolio_data = generate_mock_portfolio_data(portfolio_id)
        holdings_data = generate_mock_holdings()
        
        print("Generated data successfully")  # Debug log
        return portfolio_data, holdings_data

    @app.callback(
        Output("monitor-content", "children"),
        [Input("portfolio-data", "data"),
         Input("holdings-data", "data")]
    )
    def update_monitor_content(portfolio_data, holdings_data):
        """Update the main content area of the monitor."""
        print("\nupdate_monitor_content called")  # Debug log
        print(f"Portfolio data present: {bool(portfolio_data)}")  # Debug log
        print(f"Holdings data present: {bool(holdings_data)}")  # Debug log

        if not portfolio_data or not holdings_data:
            print("No data available")  # Debug log
            return html.Div("No portfolio data available", className="text-center p-4")

        try:
            components = []
            
            # Create summary
            print("Creating portfolio summary...")  # Debug log
            summary = create_portfolio_summary(portfolio_data)
            components.append(summary)
            
            # Create holdings table
            print("Creating holdings table...")  # Debug log
            holdings = create_holdings_table(holdings_data)
            components.append(holdings)
            
            # Create allocation charts
            print("Creating allocation charts...")  # Debug log
            charts = create_allocation_charts()
            components.append(charts)
            
            print("All components created successfully")  # Debug log
            return html.Div(components)
            
        except Exception as e:
            print(f"Error updating monitor content: {str(e)}")  # Debug log
            return html.Div(
                f"Error loading portfolio data: {str(e)}", 
                className="text-center p-4 text-danger"
            )

    @app.callback(
        [Output("asset-allocation-chart", "figure"),
         Output("geographic-allocation-chart", "figure")],
        [Input("holdings-data", "data")]
    )
    def update_allocation_charts(holdings_data):
        """Update the allocation charts."""
        print("\nupdate_allocation_charts called")  # Debug log
        print(f"Holdings data present: {bool(holdings_data)}")  # Debug log
        
        if not holdings_data:
            print("No holdings data available")  # Debug log
            return {}, {}
            
        try:
            # Prepare data for charts
            sector_data = {}
            region_data = {}
            
            for holding in holdings_data:
                # Aggregate sector data
                sector = holding.get("sector", "Other")
                sector_data[sector] = sector_data.get(sector, 0) + holding["weight"]
                
                # Aggregate region data
                region = holding.get("region", "Other")
                region_data[region] = region_data.get(region, 0) + holding["weight"]
            
            print(f"Processed holdings - Sectors: {list(sector_data.keys())}")  # Debug log
            
            # Create sector allocation chart
            sector_fig = px.pie(
                values=list(sector_data.values()),
                names=list(sector_data.keys()),
                title="Sector Allocation",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            sector_fig.update_layout(
                showlegend=True,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            
            # Create geographic allocation chart
            region_fig = px.pie(
                values=list(region_data.values()),
                names=list(region_data.keys()),
                title="Geographic Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            region_fig.update_layout(
                showlegend=True,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            
            print("Charts created successfully")  # Debug log
            return sector_fig, region_fig
            
        except Exception as e:
            print(f"Error creating allocation charts: {str(e)}")  # Debug log
            return {}, {}
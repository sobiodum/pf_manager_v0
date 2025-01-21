


"""
Callbacks for the Portfolio Builder.
File: src/callbacks/portfolio_builder_callbacks.py
"""

from dash import html, Input, Output, State, ALL, MATCH, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
import logging
logger = logging.getLogger(__name__)

def init_portfolio_builder_callbacks(app):
    """Initialize all callbacks for the portfolio builder."""
    
    @app.callback(
        Output("search-results", "children"),
        [Input("search-input", "value"),
         Input("search-input", "n_submit")],  # Trigger on Enter key
        [State("selected-instruments", "data")]
    )
    def update_search_results(search_term, n_submit, selected_instruments):
        """Update search results based on input."""
        print(f"Search triggered with term: {search_term}")  # Debug log
        
        if not search_term or len(search_term) < 3:  # Require at least 3 characters
            return []
            
        # Convert selected instruments to a set of tickers for easy lookup
        selected_tickers = {inst["ticker"] for inst in (selected_instruments or [])}
        
        # Get Bloomberg client and search
        from services.bloomberg_client import get_bloomberg_client
        client = get_bloomberg_client()
        
        # Ensure connection
        if not client.is_connected and not client.connect():
            return html.Div("Bloomberg connection failed", className="text-danger p-3")
            
        try:
            # Search for instruments
            results = client.search_securities(search_term)
            print(f"Found {len(results)} results")  # Debug log
            
            if not results:
                return html.Div(
                    "No matching instruments found",
                    className="text-muted p-3"
                )
            
            # Create results display
            return dbc.ListGroup([
                dbc.ListGroupItem([
                    dbc.Row([
                        dbc.Col([
                            html.Div(result["ticker"], className="fw-bold"),
                            html.Small(result["name"], className="text-muted d-block")
                        ], width=8),
                        dbc.Col([
                            html.Small(
                                f"Type: {result.get('security_type', 'N/A')}", 
                                className="d-block text-muted"
                            ),
                            html.Small(
                                f"Currency: {result.get('currency', 'N/A')}", 
                                className="text-muted"
                            )
                        ], width=3),
                        dbc.Col(
                            dbc.Button(
                                "Add",
                                id={"type": "add-instrument", "index": result["ticker"]},
                                color="primary",
                                size="sm",
                                disabled=result["ticker"] in selected_tickers,
                                className="float-end"
                            ),
                            width=1,
                            className="d-flex align-items-center"
                        )
                    ])
                ], className="py-2") for result in results
            ], className="mt-3")
            
        except Exception as e:
            print(f"Error during search: {str(e)}")  # Debug log
            return html.Div(
                f"Error performing search: {str(e)}", 
                className="text-danger p-3"
            )


    
    @app.callback(
    [Output("performance-chart", "figure"),
     Output("portfolio-status-message", "children")],
    [Input("generate-portfolio-btn", "n_clicks")],
    [State("selected-instruments", "data"),
     State("base-currency", "value"),
     State("time-range", "value")],
    prevent_initial_call=True)
    
    def generate_portfolio(n_clicks, instruments, currency, time_range):
        """Generate portfolio analysis when button is clicked."""
        if not n_clicks:  # Button hasn't been clicked
            return go.Figure(), ""
            
        if not instruments:
            return go.Figure(), html.Div(
                "Please select securities before generating portfolio analysis.",
                className="text-warning"
            )
        
        # Check if weights sum to 100%
        total_weight = sum(float(inst.get("weight", 0) or 0) for inst in instruments)
        if abs(total_weight - 100) > 0.01:
            return go.Figure(), html.Div(
                "Portfolio weights must sum to 100% before generating analysis.",
                className="text-danger"
            )
        
        # Convert time range to dates
        from datetime import datetime, timedelta
        end_date = datetime.now()
        
        time_ranges = {
            "6M": timedelta(days=180),
            "1Y": timedelta(days=365),
            "2Y": timedelta(days=730),
            "3Y": timedelta(days=1095),
            "4Y": timedelta(days=1460),
            "5Y": timedelta(days=1825)
        }
        
        start_date = end_date - time_ranges.get(time_range, time_ranges["1Y"])
        
        # Format dates for Bloomberg
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        
        # Prepare securities and weights
        securities = [inst["ticker"] for inst in instruments]
        weights = {inst["ticker"]: float(inst.get("weight", 0)) for inst in instruments}
        
        try:
            # Show loading message
            status = html.Div([
                dbc.Spinner(
                    size="sm", 
                    color="primary",
                    spinner_class_name="me-2"  # Changed from className to spinner_class_name
                ),
                "Downloading historical data..."
            ], className="text-primary")
            
            # Get Bloomberg client
            from services.bloomberg_client import get_bloomberg_client
            client = get_bloomberg_client()
            
            data = client.get_historical_data(
            securities=securities,
            weights=weights,
            start_date=start_date_str,
            end_date=end_date_str,
            currency=currency
            )
            
            print(f"Retrieved data for {len(data)} securities")
            if 'portfolio' in data:
                print(f"Portfolio data shape: {data['portfolio'].shape}")
            else:
                print("No portfolio data generated")

            # Check for valid data
            if not data:
                return go.Figure(), html.Div(
                    "No data available for the selected securities.",
                    className="text-warning"
                )
            
            # Create figure
            fig = go.Figure()
            
            # Add individual security traces
            for security in securities:
                if security in data:
                    df = data[security]
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['value'],
                        name=f"{security} ({weights[security]}%)",
                        mode='lines',
                        opacity=0.7
                    ))
            
            # Add portfolio trace if available
            if 'portfolio' in data:
                portfolio_df = data['portfolio']
                fig.add_trace(go.Scatter(
                    x=portfolio_df.index,
                    y=portfolio_df['portfolio_value'],
                    name='Portfolio Total',
                    mode='lines',
                    line=dict(width=3, color='yellow'),
                ))
            
            # Update layout
            fig.update_layout(
                title="Portfolio Performance",
                xaxis_title="Date",
                yaxis_title=f"Total Return Index ({currency})",
                hovermode='x unified',
                showlegend=True,
                template="plotly_dark",
                height=500
            )
            
            # Add range selector and slider
            fig.update_xaxes(rangeslider_visible=True)
            
            success_message = html.Div(
                "Portfolio analysis generated successfully!",
                className="text-success"
            )
            
            return fig, success_message
                
        except Exception as e:
            print(f"Error generating portfolio: {str(e)}")
            return go.Figure(), html.Div(
                f"Error generating portfolio: {str(e)}",
                className="text-danger"
            )
        
    def update_performance_chart(instruments, currency, time_range):
        """Update the performance chart based on selected portfolio."""
        if not instruments:
            return go.Figure()
            
        # Convert time range to dates
        from datetime import datetime, timedelta
        end_date = datetime.now()
        
        time_ranges = {
            "6M": timedelta(days=180),
            "1Y": timedelta(days=365),
            "2Y": timedelta(days=730),
            "3Y": timedelta(days=1095),
            "4Y": timedelta(days=1460),
            "5Y": timedelta(days=1825)
        }
        
        start_date = end_date - time_ranges.get(time_range, time_ranges["1Y"])
        
        # Format dates for Bloomberg
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        
        # Get Bloomberg client
        from services.bloomberg_client import get_bloomberg_client
        client = get_bloomberg_client()
        
        # Prepare securities and weights
        securities = [inst["ticker"] for inst in instruments]
        weights = {inst["ticker"]: float(inst.get("weight", 0)) for inst in instruments}
        
        try:
            data = client.get_historical_data(
            securities=securities,
            weights=weights,  # Pass weights here
            start_date=start_date_str,
            end_date=end_date_str,
            currency=currency
        )
            
            if not data:
                return go.Figure()
            
            # Create figure
            fig = go.Figure()
            
            # Add individual security traces
            for security in securities:
                if security in data:
                    df = data[security]
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['value'],
                        name=f"{security} ({weights[security]}%)",
                        mode='lines',
                        opacity=0.7
                    ))
            
            # Add portfolio trace
            if 'portfolio' in data:
                portfolio_df = data['portfolio']
                fig.add_trace(go.Scatter(
                    x=portfolio_df.index,
                    y=portfolio_df['portfolio_value'],
                    name='Portfolio Total',
                    mode='lines',
                    line=dict(width=3, color='yellow'),
                ))
            
            # Update layout
            fig.update_layout(
                title="Portfolio Performance",
                xaxis_title="Date",
                yaxis_title=f"Total Return Index ({currency})",
                hovermode='x unified',
                showlegend=True,
                template="plotly_dark",
                height=500
            )
            
            # Add range selector and slider
            fig.update_xaxes(rangeslider_visible=True)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error updating chart: {str(e)}")
            return go.Figure()

    # Add callback for allocation warning
    @app.callback(
        Output("allocation-alert", "color"),
        [Input("selected-instruments", "data")]
    )
    def update_allocation_alert(instruments):
        """Update allocation alert color based on total allocation."""
        if not instruments:
            return "primary"
            
        total_weight = sum(float(inst.get("weight", 0) or 0) for inst in instruments)
        if abs(total_weight - 100) < 0.01:  # Allow for small floating point differences
            return "success"
        return "warning"
    
    @app.callback(
        [Output("selected-instruments", "data"),
         Output("allocation-warning", "is_open")],
        [Input({"type": "add-instrument", "index": ALL}, "n_clicks"),
         Input({"type": "remove-instrument", "index": ALL}, "n_clicks"),
         Input({"type": "weight-input", "index": ALL}, "value")],
        [State("selected-instruments", "data"),
         State({"type": "add-instrument", "index": ALL}, "id")]
    )
    def update_selected_instruments(add_clicks, remove_clicks, weights, current_instruments, add_ids):
        """Handle adding and removing instruments and updating weights."""
        ctx = callback_context
        if not ctx.triggered:
            return current_instruments or [], False
            
        triggered_id = ctx.triggered[0]["prop_id"]
        current_instruments = current_instruments or []
        
        if "add-instrument" in triggered_id:
            button_idx = next((i for i, clicks in enumerate(add_clicks) if clicks), None)
            if button_idx is not None:
                ticker = add_ids[button_idx]["index"]
                if not any(inst["ticker"] == ticker for inst in current_instruments):
                    # Get Bloomberg client to fetch instrument details
                    from services.bloomberg_client import get_bloomberg_client
                    client = get_bloomberg_client()
                    results = client.search_securities(ticker)
                    
                    if results:
                        instrument = next(
                            (r for r in results if r["ticker"] == ticker), 
                            None
                        )
                        if instrument:
                            instrument["weight"] = 0  # Initialize weight
                            current_instruments.append(instrument)
                
        elif "remove-instrument" in triggered_id:
            ticker = json.loads(triggered_id.split(".")[0])["index"]
            current_instruments = [
                inst for inst in current_instruments 
                if inst["ticker"] != ticker
            ]
                                
        elif "weight-input" in triggered_id:
            # Update weights
            for i, weight in enumerate(weights):
                if i < len(current_instruments):
                    try:
                        current_instruments[i]["weight"] = float(weight) if weight else 0
                    except (ValueError, TypeError):
                        current_instruments[i]["weight"] = 0
        
        # Check total allocation
        total_weight = sum(float(inst.get("weight", 0) or 0) 
                         for inst in current_instruments)
        warning = abs(total_weight - 100) > 0.01  # Allow for small floating point differences
        
        return current_instruments, warning

    @app.callback(
        [Output("selected-instruments-display", "children"),
         Output("total-allocation", "children")],
        [Input("selected-instruments", "data")]
    )
    def update_selected_instruments_display(instruments):
        """Update the display of selected instruments and total allocation."""
        if not instruments:
            return html.Div(
                "No instruments selected", 
                className="text-muted"
            ), "0%"
            
        total_weight = sum(float(inst.get("weight", 0) or 0) for inst in instruments)
            
        table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Ticker"),
                    html.Th("Name"),
                    html.Th("Currency"),
                    html.Th("Type"),
                    html.Th("Weight (%)"),
                    html.Th("Action")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(instrument["ticker"]),
                    html.Td(instrument["name"]),
                    html.Td(instrument["currency"]),
                    html.Td(instrument.get("security_type", "N/A")),
                    html.Td(
                        dbc.Input(
                            type="number",
                            id={"type": "weight-input", "index": i},
                            value=instrument.get("weight", 0),
                            min=0,
                            max=100,
                            step=0.1,
                            size="sm"
                        ),
                        style={"width": "100px"}
                    ),
                    html.Td(
                        dbc.Button(
                            html.I(className="fas fa-times"),
                            id={"type": "remove-instrument", "index": instrument["ticker"]},
                            color="danger",
                            size="sm",
                            className="btn-icon"
                        )
                    )
                ]) for i, instrument in enumerate(instruments)
            ])
        ], bordered=True, hover=True, size="sm", className="mt-3")
        
        return table, f"{total_weight:.1f}%"


"""
Callbacks for the Portfolio Builder.
File: src/callbacks/portfolio_builder_callbacks.py
"""

from dash import html, Input, Output, State, ALL, MATCH, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from services.mock_data import search_instruments

def init_portfolio_builder_callbacks(app):
    """Initialize all callbacks for the portfolio builder."""
    
    @app.callback(
        Output("search-results", "children"),
        [Input("search-input", "value")],
        [State("selected-instruments", "data")]
    )
    def update_search_results(search_term, selected_instruments):
        """Update search results based on input."""
        if not search_term:
            return []
            
        # Convert selected instruments to a set of tickers for easy lookup
        selected_tickers = {inst["ticker"] for inst in (selected_instruments or [])}
        
        # Get search results from mock service
        results = search_instruments(search_term)
        
        # Create result items
        return dbc.ListGroup([
            dbc.ListGroupItem(
                [
                    # Ticker and name
                    dbc.Row([
                        dbc.Col([
                            html.Div(item["ticker"], className="fw-bold"),
                            html.Div(item["name"], className="small text-muted")
                        ], width=8),
                        # Add button
                        dbc.Col([
                            dbc.Button(
                                "Add",
                                id={"type": "add-instrument", "index": item["ticker"]},
                                color="primary",
                                size="sm",
                                className="float-end",
                                disabled=item["ticker"] in selected_tickers
                            )
                        ], width=4, className="d-flex align-items-center")
                    ]),
                    # Additional info
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Small("Currency: ", className="text-muted"),
                                html.Small(item["currency"])
                            ], className="me-3"),
                            html.Div([
                                html.Small("Sector: ", className="text-muted"),
                                html.Small(item["sector"])
                            ])
                        ])
                    ], className="mt-2")
                ],
                className="py-2"
            )
            for item in results
        ])

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
                    instrument = next(inst for inst in search_instruments(ticker) 
                                   if inst["ticker"] == ticker)
                    instrument["weight"] = 0  # Initialize weight
                    current_instruments.append(instrument)
                
        elif "remove-instrument" in triggered_id:
            ticker = json.loads(triggered_id.split(".")[0])["index"]
            current_instruments = [inst for inst in current_instruments 
                                if inst["ticker"] != ticker]
                                
        elif "weight-input" in triggered_id:
            # Update weights
            for i, weight in enumerate(weights):
                if i < len(current_instruments):
                    current_instruments[i]["weight"] = float(weight) if weight is not None else 0
        
        # Check total allocation
        total_weight = sum(float(inst.get("weight", 0) or 0) for inst in current_instruments)
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
            return html.Div("No instruments selected", className="text-muted"), "0%"
            
        total_weight = sum(float(inst.get("weight", 0) or 0) for inst in instruments)
            
        table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Ticker"),
                    html.Th("Name"),
                    html.Th("Currency"),
                    html.Th("Sector"),
                    html.Th("Weight (%)"),
                    html.Th("Action")
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td(instrument["ticker"]),
                    html.Td(instrument["name"]),
                    html.Td(instrument["currency"]),
                    html.Td(instrument["sector"]),
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
                    ),
                    html.Td(
                        dbc.Button(
                            "Remove",
                            id={"type": "remove-instrument", "index": instrument["ticker"]},
                            color="danger",
                            size="sm"
                        )
                    )
                ])
                for i, instrument in enumerate(instruments)
            ])
        ], bordered=True, hover=True, size="sm", className="mt-3")
        
        return table, f"{total_weight:.1f}%"
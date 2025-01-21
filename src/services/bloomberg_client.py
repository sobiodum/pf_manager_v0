"""
Bloomberg Terminal API client implementation.
File: src/services/bloomberg_client.py
"""

import blpapi
from typing import List, Dict, Optional
import logging
from datetime import datetime
import pandas as pd
import os

logger = logging.getLogger(__name__)

# Create file handler
file_handler = logging.FileHandler('bloomberg_client.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)


"""
Bloomberg Terminal API client implementation.
File: src/services/bloomberg_client.py
"""


class BloombergClient:
    """Client for interacting with the Bloomberg Terminal API."""
    
    def __init__(self):
        """Initialize the Bloomberg API client."""
        self.session = None
        self._reference_data_service = None
        self.is_connected = False

    def connect(self) -> bool:
        """
        Establish connection to Bloomberg Terminal.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Initialize session options
            sessionOptions = blpapi.SessionOptions()
            sessionOptions.setServerHost("localhost")
            sessionOptions.setServerPort(8194)
            
            # Create a Session
            logger.info("Creating Bloomberg API session...")
            self.session = blpapi.Session(sessionOptions)
            
            # Start session
            if not self.session.start():
                logger.error("Failed to start Bloomberg session.")
                return False
            
            # Open reference data service
            if not self.session.openService("//blp/refdata"):
                logger.error("Failed to open reference data service.")
                return False

            self._reference_data_service = self.session.getService("//blp/refdata")
            self.is_connected = True
            logger.info("Successfully connected to Bloomberg Terminal")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to Bloomberg: {str(e)}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Disconnect from Bloomberg Terminal."""
        if self.session:
            self.session.stop()
            self.is_connected = False
            logger.info("Disconnected from Bloomberg Terminal")

    def get_historical_data(self, securities: List[str], weights: Dict[str, float], start_date: str, end_date: str, currency: str = "USD") -> Dict:
        """
        Get historical total return data for specified securities.
        
        Args:
            securities: List of security identifiers
            weights: Dictionary mapping security identifiers to their weights (in percent)
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            currency: Base currency for the data
            
        Returns:
            Dict with security data and saves to CSV
        """
        print('getting historical data')
        os.makedirs("data", exist_ok=True)
        
        cleaned_weights = {}
        for security, weight in weights.items():
            cleaned_security = security.replace("<equity>", " Equity").replace("  ", " ")
            cleaned_weights[cleaned_security] = weight
        
        if not self._reference_data_service:
            logger.error("Reference data service not available")
            return {}

        try:
            request = self._reference_data_service.createRequest("HistoricalDataRequest")
            
            # Add securities
            for security in securities:
                clean_security = security.replace("<equity>", " Equity").replace("  ", " ")
                request.getElement("securities").appendValue(clean_security)
                
            # Add total return field
            request.getElement("fields").appendValue("TOT_RETURN_INDEX_GROSS_DVDS")
                
            # Set dates and currency
            request.set("startDate", start_date)
            request.set("endDate", end_date)
            request.set("periodicitySelection", "DAILY")
             # Add required elements from documentation
            request.set("nonTradingDayFillOption", "ACTIVE_DAYS_ONLY")
            request.set("nonTradingDayFillMethod", "PREVIOUS_VALUE")
            request.set("overrideOption", "OVERRIDE_OPTION_CLOSE")
            
            if currency != "USD":
                request.set("currency", currency)

            logger.info(f"Sending historical data request for {len(securities)} securities")
            self.session.sendRequest(request)
            print(f'reques send: {request}')
            

            
            
            response_data = {}
            print(f'Starting data processing for {len(securities)} securities')
            
            while True:
                ev = self.session.nextEvent(500)
                
                for msg in ev:
                    print(f'Processing message type: {msg.messageType()}')
                    if msg.hasElement("securityData"):
                        security_data = msg.getElement("securityData")
                        security = security_data.getElementAsString("security")
                        print(f'Processing data for security: {security}')
                        
                        # Initialize data for this security
                        dates = []
                        values = []
                        
                        # Get the field data
                        field_data = security_data.getElement("fieldData")
                        num_points = field_data.numValues()
                        print(f'Found {num_points} data points for {security}')
                        
                        # Process each data point
                        for i in range(field_data.numValues()):
                            point = field_data.getValueAsElement(i)
                            date = point.getElementAsString("date")
                            
                            if point.hasElement("TOT_RETURN_INDEX_GROSS_DVDS"):
                                value = point.getElementAsFloat("TOT_RETURN_INDEX_GROSS_DVDS")
                                dates.append(date)
                                values.append(value)
                        
                        # Store data in DataFrame
                        df = pd.DataFrame({
                            'date': dates,
                            'value': values
                        })
                        print(f'Created DataFrame for {security} with {len(df)} rows')
                        df['date'] = pd.to_datetime(df['date'])
                        df.set_index('date', inplace=True)
                        
                        # Save individual security data
                        try:
                            csv_filename = f"data/{security.replace(' ', '_')}_{currency}_{start_date}_{end_date}.csv"
                            df.to_csv(csv_filename)
                            print(f'Successfully saved data for {security} to {csv_filename}')
                        except Exception as e:
                            logger.error(f"Failed to save CSV for {security}: {str(e)}")
                        
                        response_data[security] = df
                
                if ev.eventType() == blpapi.Event.RESPONSE:
                    print('Received final RESPONSE event')
                    break
            
            print(f'Completed data collection. Found data for {len(response_data)} securities')
            
            # Calculate and save portfolio timeseries if we have data
            if response_data:
                print("Data verification:")
                for security, df in response_data.items():
                    print(f"{security}: {len(df)} rows, date range: {df.index.min()} to {df.index.max()}")
                print('Calculating portfolio timeseries')
                # Pass cleaned weights to calculation
                portfolio_df = self._calculate_portfolio_timeseries(response_data, cleaned_weights)
                portfolio_filename = f"data/portfolio_{currency}_{start_date}_{end_date}.csv"
                portfolio_df.to_csv(portfolio_filename)
                print(f'Saved portfolio data to {portfolio_filename}')
                
                response_data['portfolio'] = portfolio_df
                print('Added portfolio data to response')
                    
            return response_data

        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            return {}

    def _calculate_portfolio_timeseries(self, security_data: Dict[str, pd.DataFrame], weights: Dict[str, float]) -> pd.DataFrame:
        """
        Calculate weighted portfolio timeseries with rebased values.
        Each security's timeseries is rebased to 100 at the start date.
        """
        try:
            # Get all dates from all securities
            all_dates = pd.DatetimeIndex([])
            for df in security_data.values():
                all_dates = all_dates.union(df.index)
            all_dates = all_dates.sort_values()
            
            # Create empty DataFrame with all dates
            portfolio_df = pd.DataFrame(index=all_dates)
            
            # Add normalized and weighted securities
            for security, df in security_data.items():
                if security in weights:
                    print(f"Processing security {security} with weight {weights[security]}")
                    weight = weights[security] / 100.0
                    
                    # Reindex to align dates and fill missing values
                    aligned_series = df['value'].reindex(all_dates).fillna(method='ffill')
                    
                    # Normalize series to 100 at start date
                    initial_value = aligned_series.iloc[0]
                    normalized_series = (aligned_series / initial_value) * 100
                    
                    # Apply weight to normalized series
                    portfolio_df[security] = normalized_series * weight
                    print(f"Added weighted series for {security}:")
                    print(f"Initial value: {initial_value:.2f}")
                    print(f"Normalized range - Min: {normalized_series.min():.2f}, Max: {normalized_series.max():.2f}")
                    print(f"Weighted range - Min: {portfolio_df[security].min():.2f}, Max: {portfolio_df[security].max():.2f}")
                else:
                    print(f"Warning: Security {security} not found in weights dictionary {weights}")
            
            # Calculate portfolio total
            portfolio_df['portfolio_value'] = portfolio_df.sum(axis=1)
            print(f"Portfolio calculation complete. Shape: {portfolio_df.shape}")
            print(f"Portfolio value range - Min: {portfolio_df['portfolio_value'].min():.2f}, Max: {portfolio_df['portfolio_value'].max():.2f}")
            
            return portfolio_df
                
        except Exception as e:
            print(f"Error in portfolio calculation: {str(e)}")
            return pd.DataFrame()

        
    def search_securities(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search for securities using Bloomberg's API.
        
        Args:
            query (str): Search query string
            max_results (int): Maximum number of results to return
                
        Returns:
            List[Dict]: List of security information dictionaries
        """
        if not self.is_connected:
            logger.error("Not connected to Bloomberg")
            return []

        try:
            # First open the instruments service
            if not self.session.openService("//blp/instruments"):
                logger.error("Failed to open //blp/instruments service")
                return []
                
            instrumentsService = self.session.getService("//blp/instruments")
            
            # Create instruments search request
            request = instrumentsService.createRequest("instrumentListRequest")
            request.set("query", query)
            request.set("maxResults", max_results)
            
            logger.info(f"Sending security search request for query: {query}")
            self.session.sendRequest(request)
            
            results = []
            while True:
                event = self.session.nextEvent(500)
                
                for msg in event:
                    if msg.messageType() == blpapi.Name("InstrumentListResponse"):
                        instruments = msg.getElement("results")
                        for i in range(instruments.numValues()):
                            instrument = instruments.getValueAsElement(i)
                            security_info = {
                                "ticker": instrument.getElementAsString("security"),
                                "name": instrument.getElementAsString("description") if instrument.hasElement("description") else "",
                                "security_type": instrument.getElementAsString("securityType") if instrument.hasElement("securityType") else "",
                                "currency": instrument.getElementAsString("currency") if instrument.hasElement("currency") else "",
                                "exchange": instrument.getElementAsString("exchange") if instrument.hasElement("exchange") else "",
                                "market_sector": instrument.getElementAsString("marketSector") if instrument.hasElement("marketSector") else ""
                            }
                            results.append(security_info)
                
                if event.eventType() == blpapi.Event.RESPONSE:
                    break
                    
            logger.info(f"Found {len(results)} matching securities")
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error during security search: {str(e)}")
            return []


    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

# Create a singleton instance
_bloomberg_client = None

def get_bloomberg_client() -> BloombergClient:
    """
    Get or create the Bloomberg client singleton instance.
    
    Returns:
        BloombergClient: The Bloomberg client instance
    """
    global _bloomberg_client
    if _bloomberg_client is None:
        _bloomberg_client = BloombergClient()
    return _bloomberg_client
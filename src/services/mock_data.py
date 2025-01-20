"""
Mock data service for development without Bloomberg access.
File: src/services/mock_data.py
"""

# Sample instrument data to simulate Bloomberg results
MOCK_INSTRUMENTS = [
    {"ticker": "AAPL US Equity", "name": "Apple Inc", "currency": "USD", "sector": "Technology"},
    {"ticker": "MSFT US Equity", "name": "Microsoft Corp", "currency": "USD", "sector": "Technology"},
    {"ticker": "GOOGL US Equity", "name": "Alphabet Inc", "currency": "USD", "sector": "Technology"},
    {"ticker": "AMZN US Equity", "name": "Amazon.com Inc", "currency": "USD", "sector": "Consumer Discretionary"},
    {"ticker": "META US Equity", "name": "Meta Platforms Inc", "currency": "USD", "sector": "Technology"},
    {"ticker": "TSLA US Equity", "name": "Tesla Inc", "currency": "USD", "sector": "Consumer Discretionary"},
    {"ticker": "NVDA US Equity", "name": "NVIDIA Corp", "currency": "USD", "sector": "Technology"},
    {"ticker": "BRK/B US Equity", "name": "Berkshire Hathaway", "currency": "USD", "sector": "Financials"},
    {"ticker": "JPM US Equity", "name": "JPMorgan Chase", "currency": "USD", "sector": "Financials"},
    {"ticker": "JNJ US Equity", "name": "Johnson & Johnson", "currency": "USD", "sector": "Healthcare"}
]

def search_instruments(query: str, limit: int = 10) -> list:
    """
    Mock instrument search function.
    
    Args:
        query (str): Search term
        limit (int): Maximum number of results to return
        
    Returns:
        list: List of matching instruments
    """
    if not query:
        return []
        
    query = query.lower()
    results = []
    
    for instrument in MOCK_INSTRUMENTS:
        if (query in instrument["ticker"].lower() or 
            query in instrument["name"].lower()):
            results.append(instrument)
            
        if len(results) >= limit:
            break
            
    return results
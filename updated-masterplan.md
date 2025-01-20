# Updated Portfolio Analysis Tool Masterplan

## 1. Overview

A sophisticated local application that integrates with Bloomberg Terminal for portfolio analysis and monitoring, featuring:

- Dark theme professional interface with corporate branding
- Responsive single-page application using Plotly Dash
- Navigation system for multiple views
- Bloomberg connection status monitoring
- Comprehensive portfolio building and monitoring capabilities

## 2. Core Components

### 2.1 Navigation & Layout

- Collapsible navigation menu
- Fixed header containing:
  - Bloomberg connection status indicator
  - Reconnection button when disconnected
  - Corporate logo (small version)
  - Last data update timestamp
- Three main views:
  1. Landing Page
  2. Portfolio Builder
  3. Portfolio Monitoring

### 2.2 Landing Page

- Corporate logo prominently displayed
- Quick access buttons to main views:
  - "Create New Portfolio" (Portfolio Builder)
  - "View Active Portfolios" (Portfolio Monitoring)
- Future expansion:
  - Dashboard with benchmark charts/indices
  - Recent portfolio performance summaries
  - Market overview

### 2.3 Portfolio Builder

#### Search & Selection
- Bloomberg instrument search:
  - Free text search with BBG API integration
  - Display top 20 results showing:
    - Bloomberg Ticker
    - Name
    - Currency (CURNCY field)
  - Cache recent searches for quick access
  - Save search history

#### Portfolio Configuration
- Base currency selection (USD, EUR, CHF)
- Time range selection (6M, 1Y, 2Y, 3Y, 4Y, 5Y, max)
- Allocation input for each instrument
- Warning if allocations don't sum to 100%

#### Data Display
- Interactive performance chart:
  - Zoom functionality
  - Detailed tooltips
  - Instrument toggling
  - Data export capability
- Collapsible metrics table showing:
  - Sharpe ratio (using 2.5% fixed risk-free rate)
  - Volatility
  - Annualized return
  - Maximum drawdown
  - Calculated for different periods (YTD, 1Y, 3Y, 5Y) where data available

#### Portfolio Comparison (Future Feature)
- Overlay multiple portfolio performance charts
- Show return differences
- Compare key statistics side by side

### 2.4 Portfolio Monitoring

#### Portfolio Summary
- Large format display of:
  - Total portfolio value
  - Portfolio name
  - P&L in % and reference currency (USD)
  - Day's change
  - Mini sparkline showing recent performance

#### Holdings Table
- Main table showing:
  - Instrument details
  - P&L in three formats:
    1. Local currency
    2. Portfolio reference currency
    3. Percentage (local currency)
  - Weighted average cost basis
  - Collapsible details showing individual trades
- Manual trade entry:
  - Date selection via calendar
  - Purchase/sale price
  - Number of shares
  - Multiple trades per instrument

#### Portfolio Analysis
- Doughnut charts showing current allocations:
  - Geographic
  - Asset class
  - Other Bloomberg classifications
- Update with price refreshes
- Future feature: Deviation from benchmark visualization

## 3. Technical Architecture

### 3.1 Framework
- Plotly Dash for sophisticated UI and interactive visualizations
- Dark theme implementation throughout

### 3.2 Data Management
- CSV-based storage system:
  - Individual instrument data files
  - Portfolio configuration files
  - Metadata including creation and update timestamps
- Intelligent data refresh:
  - Only update visible view data
  - Include last saved date in new data pulls
  - Track API usage
  - Support offline mode with cached data

### 3.3 Bloomberg Integration
- Connection status monitoring
- Manual reconnection capability
- Data caching for offline usage
- Field requirements as per original spec

### 3.4 Performance Optimization
- Efficient data storage and retrieval
- Minimal API calls
- Smart update strategy
- Background processing for data fetching

## 4. Implementation Phases

### Phase 1: Core Infrastructure
- Basic navigation setup
- Bloomberg connection handling
- Data storage system
- Dark theme implementation

### Phase 2: Portfolio Builder
- Instrument search and selection
- Portfolio configuration
- Basic charting
- Performance metrics

### Phase 3: Portfolio Monitoring
- Holdings table
- P&L tracking
- Trade entry system
- Allocation visualizations

### Phase 4: Enhanced Features
- Interactive charts
- Detailed metrics
- Portfolio comparison
- Offline mode capabilities

### Phase 5: Polish & Optimization
- UI refinements
- Performance optimization
- Corporate branding
- PDF export capability

## 5. Future Considerations

### 5.1 Potential Extensions
- Advanced portfolio analytics
- Real-time price updates
- Benchmark tracking
- Tax reporting
- Additional visualization types

### 5.2 Technical Upgrades
- Database migration path
- Advanced caching strategies
- Additional data providers
- API usage optimization

## 6. Notes & Constraints

- Local Windows deployment only
- Single user system
- Bloomberg Terminal required
- Manual data refresh approach
- Offline functionality support
- Focus on maintainability and extensibility
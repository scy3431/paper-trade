# Stock Trading Simulator

A beginner-friendly web application that lets users practice stock trading with virtual money. No signup required - just start trading immediately!

## Features

- **Interactive Stock Charts**: View real-time stock data with 6-month historical charts
- **Technical Indicators**: Built-in SMA (Simple Moving Average) 20 and 50-day lines, plus RSI (Relative Strength Index)
- **Paper Trading**: Buy and sell stocks using virtual money ($10,000 starting balance)
- **Portfolio Tracking**: Monitor your positions, gains/losses, and transaction history
- **Real Stock Data**: Powered by Yahoo Finance API for accurate market data
- **Clean Interface**: Modern, responsive design that works on desktop and mobile
- **No Registration**: Start trading immediately without any signup process

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## How to Use

### Getting Started
1. **Search for a stock**: Enter a stock symbol (e.g., AAPL, MSFT, GOOGL, TSLA) in the search box
2. **View the chart**: See the 6-month price history with technical indicators
3. **Check stock info**: View current price, sector, market cap, and P/E ratio
4. **Place trades**: Use the trading form to buy or sell shares

### Trading Features
- **Buy Orders**: Purchase shares with your virtual cash
- **Sell Orders**: Sell shares you own to realize gains/losses
- **Portfolio Tracking**: Monitor your total portfolio value and individual positions
- **Transaction History**: View your recent buy/sell transactions

### Technical Indicators
- **SMA 20**: 20-day Simple Moving Average (red line)
- **SMA 50**: 50-day Simple Moving Average (blue line)
- **Price Chart**: Actual stock price (purple line)

## Supported Stocks

The app works with any stock symbol available on Yahoo Finance, including:
- **Tech**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, AMD
- **Entertainment**: NFLX, DIS
- **And more!**

## Technical Details

### Backend
- **Flask**: Web framework for the API
- **yfinance**: Yahoo Finance API for real-time stock data
- **pandas**: Data manipulation and technical indicator calculations
- **numpy**: Numerical computations

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Interactive charts and real-time updates
- **Chart.js**: Beautiful, interactive stock charts
- **No external frameworks**

### API Endpoints
- `GET /api/stock/<symbol>`: Get stock data and technical indicators
- `GET /api/portfolio`: Get current portfolio status
- `POST /api/trade`: Execute buy/sell trades
- `GET /api/search/<query>`: Search for stocks

## Features in Detail

### Interactive Charts
- 6-month historical price data
- Multiple technical indicators
- Responsive design
- Hover tooltips with price information

### Portfolio Management
- Real-time portfolio value calculation
- Position tracking with average cost basis
- Gain/loss calculations
- Transaction history

### Trading System
- Virtual money system ($10,000 starting balance)
- Buy/sell order execution
- Insufficient funds protection
- Position averaging for multiple buys

## Customization

### Starting Balance
To change the starting cash amount, edit the `user_portfolio` variable in `app.py`:
```python
user_portfolio = {
    'cash': 10000.0,  # Change this value
    'positions': {},
    'transactions': []
}
```

### Chart Period
To change the historical data period, modify the `timedelta` in the `get_stock_data` function:
```python
start_date = end_date - timedelta(days=180)  # Change 180 to desired days
```


### Common Issues

1. **"No data found for this symbol"**
   - Check that the stock symbol is correct
   - Try popular symbols like AAPL, MSFT, GOOGL

2. **"Error fetching stock data"**
   - Check your internet connection
   - The Yahoo Finance API might be temporarily unavailable

3. **Port installation issues**
   - Make sure you have Python 3.7+ installed
   - Try: `python -m pip install -r requirements.txt`

### Dependencies Issues
If you encounter dependency conflicts, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```


---


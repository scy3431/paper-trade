from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# Global variable to store user's portfolio (in a real app, this would be a database)
user_portfolio = {
    'cash': 10000.0,  # Starting with $10,000
    'positions': {},   # {symbol: {'shares': quantity, 'avg_price': price}}
    'transactions': [] # List of buy/sell transactions
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    try:
        # Get stock data using yfinance
        stock = yf.Ticker(symbol.upper())
        hist = stock.info
        
        # Get historical data for the last 6 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        historical_data = stock.history(start=start_date, end=end_date)
        
        if historical_data.empty:
            return jsonify({'error': 'No data found for this symbol'}), 404
        
        # Calculate technical indicators
        data = calculate_technical_indicators(historical_data)
        
        # Format data for frontend (optimized)
        chart_data = []
        for index, row in data.iterrows():
            chart_data.append({
                'date': index.strftime('%Y-%m-%d'),
                'close': float(row['Close']),
                'sma_20': float(row['SMA_20']) if not pd.isna(row['SMA_20']) else None,
                'sma_50': float(row['SMA_50']) if not pd.isna(row['SMA_50']) else None
            })
        
        return jsonify({
            'symbol': symbol.upper(),
            'info': {
                'name': hist.get('longName', 'Unknown'),
                'sector': hist.get('sector', 'Unknown'),
                'market_cap': hist.get('marketCap', 0),
                'pe_ratio': hist.get('trailingPE', 0),
                'dividend_yield': hist.get('dividendYield', 0),
                'current_price': float(historical_data['Close'].iloc[-1])
            },
            'data': chart_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_technical_indicators(data):
    """Calculate technical indicators for the stock data"""
    # Simple Moving Averages
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # RSI (Relative Strength Index)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    return data

@app.route('/api/portfolio')
def get_portfolio():
    """Get current portfolio status"""
    total_value = user_portfolio['cash']
    positions_value = 0
    
    # Calculate current value of all positions
    for symbol, position in user_portfolio['positions'].items():
        try:
            stock = yf.Ticker(symbol)
            current_price = stock.info.get('regularMarketPrice', 0)
            if current_price:
                position_value = position['shares'] * current_price
                positions_value += position_value
                position['current_price'] = current_price
                position['current_value'] = position_value
                position['gain_loss'] = position_value - (position['shares'] * position['avg_price'])
        except:
            pass
    
    total_value += positions_value
    
    return jsonify({
        'cash': user_portfolio['cash'],
        'total_value': total_value,
        'positions': user_portfolio['positions'],
        'transactions': user_portfolio['transactions'][-10:]  # Last 10 transactions
    })

@app.route('/api/trade', methods=['POST'])
def execute_trade():
    """Execute a buy or sell trade"""
    data = request.get_json()
    action = data.get('action')  # 'buy' or 'sell'
    symbol = data.get('symbol').upper()
    shares = int(data.get('shares'))
    
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.info.get('regularMarketPrice', 0)
        
        if not current_price:
            return jsonify({'error': 'Unable to get current price'}), 400
        
        if action == 'buy':
            total_cost = shares * current_price
            if total_cost > user_portfolio['cash']:
                return jsonify({'error': 'Insufficient funds'}), 400
            
            # Update portfolio
            user_portfolio['cash'] -= total_cost
            
            if symbol in user_portfolio['positions']:
                # Update existing position
                current_shares = user_portfolio['positions'][symbol]['shares']
                current_avg_price = user_portfolio['positions'][symbol]['avg_price']
                total_shares = current_shares + shares
                new_avg_price = ((current_shares * current_avg_price) + (shares * current_price)) / total_shares
                
                user_portfolio['positions'][symbol] = {
                    'shares': total_shares,
                    'avg_price': new_avg_price
                }
            else:
                # New position
                user_portfolio['positions'][symbol] = {
                    'shares': shares,
                    'avg_price': current_price
                }
        
        elif action == 'sell':
            if symbol not in user_portfolio['positions']:
                return jsonify({'error': 'No shares to sell'}), 400
            
            if user_portfolio['positions'][symbol]['shares'] < shares:
                return jsonify({'error': 'Not enough shares to sell'}), 400
            
            # Update portfolio
            total_proceeds = shares * current_price
            user_portfolio['cash'] += total_proceeds
            
            remaining_shares = user_portfolio['positions'][symbol]['shares'] - shares
            if remaining_shares == 0:
                del user_portfolio['positions'][symbol]
            else:
                user_portfolio['positions'][symbol]['shares'] = remaining_shares
        
        # Record transaction
        transaction = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'symbol': symbol,
            'shares': shares,
            'price': current_price,
            'total': shares * current_price
        }
        user_portfolio['transactions'].append(transaction)
        
        return jsonify({'success': True, 'message': f'{action.capitalize()} order executed successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio/update', methods=['POST'])
def update_portfolio_balance():
    """Update the user's cash balance"""
    data = request.get_json()
    new_balance = data.get('cash_balance')
    
    if new_balance is None or not isinstance(new_balance, (int, float)) or new_balance < 0:
        return jsonify({'error': 'Invalid cash balance'}), 400
    
    user_portfolio['cash'] = float(new_balance)
    
    return jsonify({
        'success': True,
        'message': f'Portfolio balance updated to ${new_balance:.2f}',
        'cash': user_portfolio['cash']
    })

@app.route('/api/portfolio/reset', methods=['POST'])
def reset_portfolio():
    """Reset the portfolio to initial state"""
    global user_portfolio
    
    # Reset to initial state
    user_portfolio = {
        'cash': 10000.0,
        'positions': {},
        'transactions': []
    }
    
    return jsonify({
        'success': True,
        'message': 'Portfolio reset successfully to $10,000',
        'cash': user_portfolio['cash']
    })

@app.route('/api/search/<query>')
def search_stocks(query):
    """Search for stocks by symbol or company name"""
    try:
        # This is a simplified search - in a real app, you'd use a proper stock database
        # For now, we'll just return some popular stocks that match the query
        popular_stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation'},
            {'symbol': 'AMD', 'name': 'Advanced Micro Devices Inc.'},
            {'symbol': 'NFLX', 'name': 'Netflix Inc.'},
            {'symbol': 'DIS', 'name': 'The Walt Disney Company'}
        ]
        
        results = []
        query_upper = query.upper()
        
        for stock in popular_stocks:
            if query_upper in stock['symbol'] or query_upper in stock['name'].upper():
                results.append(stock)
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
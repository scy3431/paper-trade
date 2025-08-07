#!/usr/bin/env python3
"""
Stock Trading Simulator - Quick Start Script
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'yfinance', 'pandas', 'numpy']
    
    print("🔍 Checking dependencies...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f" {package}")
        except ImportError:
            print(f" {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print(" Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print(" Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    return True

def start_app():
    """Start the Flask application"""
    print("\n Starting Stock Trading Simulator...")
    print(" Features:")
    print("   • Interactive stock charts with technical indicators")
    print("   • Paper trading with virtual money")
    print("   • Real-time portfolio tracking")
    print("   • No signup required")
    
    print("\n Opening browser in 3 seconds...")
    time.sleep(3)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:5000')
    except:
        print("💡 Please manually open: http://localhost:5000")
    
    print("\n How to use:")
    print("   1. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL)")
    print("   2. View the interactive chart and stock information")
    print("   3. Place buy/sell orders with your virtual money")
    print("   4. Track your portfolio performance")
    
    print("\n  Press Ctrl+C to stop the server")
    
    # Start Flask app
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n Thanks for using Stock Trading Simulator!")

if __name__ == "__main__":
    print(" Stock Trading Simulator")
    print("=" * 40)
    
    if check_dependencies():
        start_app()
    else:
        print("\n Please install dependencies first:")
        print("   pip install -r requirements.txt")

        sys.exit(1) 

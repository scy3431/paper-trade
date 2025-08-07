import requests
import json

def test_app():
    """Test the Flask application endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Stock Trading Simulator...")
    
    # Test 1: Check if app is running
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ App is running successfully!")
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the app. Make sure it's running on http://localhost:5000")
        return
    
    # Test 2: Test stock data endpoint
    try:
        response = requests.get(f"{base_url}/api/stock/AAPL")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stock data endpoint working - Got data for {data['symbol']}")
        else:
            print(f"❌ Stock data endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stock data test failed: {e}")
    
    # Test 3: Test portfolio endpoint
    try:
        response = requests.get(f"{base_url}/api/portfolio")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Portfolio endpoint working - Cash: ${data['cash']:.2f}")
        else:
            print(f"❌ Portfolio endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Portfolio test failed: {e}")
    
    print("\n🎉 Testing complete! Open http://localhost:5000 in your browser to use the app.")

if __name__ == "__main__":
    test_app() 
from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/api/stock', methods=['GET'])
def get_stock():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker not provided'}), 400

    stock = yf.Ticker(ticker)
    stock_info = stock.info
    todays_data = stock.history(period='1d')

    if 'symbol' not in stock_info:
        return jsonify({'error': 'Invalid ticker symbol'}), 400

    stock_data = {
        "symbol": stock_info.get("symbol", "N/A"),
        "companyName": stock_info.get("longName", "N/A"),
        "latestPrice": todays_data['Close'][0] if not todays_data.empty else "N/A",
        "change": stock_info.get("regularMarketChangePercent", "N/A"),
        "high": todays_data['High'][0] if not todays_data.empty else "N/A",
        "low": todays_data['Low'][0] if not todays_data.empty else "N/A",
        "logoURL": stock_info.get("logo_url", "N/A")
    }

    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)

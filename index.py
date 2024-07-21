from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/api/stock', methods=['GET'])
def get_stock():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    stock = yf.Ticker(ticker)
    stock_info = stock.info
    todays_data = stock.history(period='1d')

    stock_data = {
        "symbol": stock_info.get("symbol"),
        "companyName": stock_info.get("longName"),
        "latestPrice": todays_data['Close'][0],
        "change": stock_info.get("regularMarketChangePercent"),
        "high": todays_data['High'][0],
        "low": todays_data['Low'][0],
        "logoURL": stock_info.get("logo_url")
    }

    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)

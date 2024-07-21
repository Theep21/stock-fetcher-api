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

import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/stock', methods=['GET'])
def get_stock():
    logging.debug(f"Received request: {request.args}")
    ticker = request.args.get('ticker')
    if not ticker:
        logging.error("Ticker is required")
        return jsonify({'error': 'Ticker is required'}), 400
    try:
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
        logging.debug(f"Stock data: {stock_data}")
        return jsonify(stock_data)
    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")
        return jsonify({'error': 'Error fetching stock data'}), 500


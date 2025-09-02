from flask import request, jsonify
from Extras.db import db
from Models.stock_model import StockModel
from twelvedata import TDClient
from dotenv import load_dotenv
import os

load_dotenv()
TD_API_KEY = os.getenv("TWELVEDATA_API_KEY")
td = TDClient(apikey=TD_API_KEY)

def update_stock_price():
    data = request.json
    symbol = data.get("symbol")
    exchange = data.get("exchange")
    currency = data.get("currency", "USD")

    if not symbol or not exchange:
        return jsonify({"error": "Symbol and exchange are required"}), 400

    try:
        ts = td.price(symbol=symbol.upper()).as_json()
        price = float(ts["price"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    stock = StockModel.query.filter_by(symbol=symbol.upper()).first()
    if stock:
        stock.price = price
        stock.exchange = exchange
        stock.currency = currency
    else:
        stock = StockModel(symbol=symbol, exchange=exchange, currency=currency, price=price)
        db.session.add(stock)

    db.session.commit()
    return jsonify(stock.json()), 200  

def get_stock(symbol):
    ts = td.price(symbol=symbol.upper()).as_json()
    price = float(ts["price"])
    stock = StockModel(symbol=symbol, exchange="NASDAQ", currency="USD", price=price)
    
    stockindb = StockModel.query.filter_by(symbol=symbol.upper()).first()
    if stockindb:
        stockindb.price = price
        stockindb.exchange = "NASDAQ"
        stockindb.currency = "USD"
    else:
        stockindb = stock
    
    db.session.add(stockindb)
    db.session.commit()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock.json()), 200

def get_graphic(symbol, ammount):
    ts = td.time_series(
        symbol=f"{symbol}",
        interval="1h",
        outputsize=ammount
    )
    
    print(ts.as_json())
    return jsonify(ts.as_json())
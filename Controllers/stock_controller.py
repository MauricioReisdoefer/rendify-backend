from flask import request, jsonify
from Extras.db import db
from Models.stock_model import StockModel
from api_keys import get_td_client


def update_stock_price():
    data = request.json
    symbol = data.get("symbol")
    exchange = data.get("exchange")
    currency = data.get("currency", "USD")

    if not symbol or not exchange:
        return jsonify({"error": "Symbol and exchange are required"}), 400

    td = get_td_client()
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
    td = get_td_client()  # usa o client rotativo

    try:
        ts = td.price(symbol=symbol.upper()).as_json()
        price = float(ts["price"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

    return jsonify(stockindb.json()), 200


def get_graphic(symbol, ammount):
    td = get_td_client()

    try:
        ts = td.time_series(
            symbol=symbol,
            interval="1h",
            outputsize=ammount
        )
        return jsonify(ts.as_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_company(symbol):
    td = get_td_client()

    try:
        profile = td.company_profile(symbol=symbol.upper()).as_json()
        company_name = profile.get("name")
        if not company_name:
            return jsonify({"error": "Company name not found"}), 404
        return jsonify({"symbol": symbol.upper(), "company_name": company_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
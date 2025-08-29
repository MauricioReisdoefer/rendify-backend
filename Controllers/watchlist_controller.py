from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Extras.db import db
from Models.watchlist_model import WatchlistModel
from Models.user_model import UserModel
from Controllers.stock_controller import get_stock  

@jwt_required()
def add_or_update_watchlist():
    user_id = get_jwt_identity() 
    data = request.json
    symbol = data.get("symbol")
    exchange = data.get("exchange")
    currency = data.get("currency", "USD")

    if not symbol or not exchange:
        return jsonify({"error": "Symbol and exchange are required"}), 400

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    stock_response, status = get_stock(symbol)
    if status != 200:
        return jsonify({"error": "Stock not found"}), 404

    stock_data = stock_response.get_json()
    price = stock_data["price"]

    watch = WatchlistModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if watch:
        watch.price = price
        watch.exchange = exchange
        watch.currency = currency
    else:
        watch = WatchlistModel(symbol=symbol, exchange=exchange, currency=currency, price=price, user=user)
        db.session.add(watch)

    db.session.commit()
    return jsonify(watch.json()), 200

@jwt_required()
def get_watchlist(symbol):
    user_id = get_jwt_identity()
    watch = WatchlistModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if not watch:
        return jsonify({"error": "Watchlist item not found"}), 404
    return jsonify(watch.json()), 200

@jwt_required()
def get_all_watchlists():
    user_id = get_jwt_identity()
    watches = WatchlistModel.query.filter_by(user_id=user_id).all()
    return jsonify([w.json() for w in watches]), 200

@jwt_required()
def delete_watchlist(symbol):
    user_id = get_jwt_identity()
    watch = WatchlistModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if not watch:
        return jsonify({"error": "Watchlist item not found"}), 404
    db.session.delete(watch)
    db.session.commit()
    return jsonify({"message": "Watchlist item deleted successfully"}), 200

from flask import Blueprint, request, jsonify
from Models import user_model as UserModel
from Models.watchlist_model import Watchlist
from Extras import db
from Controllers import stock_controller

def add_to_watchlist(user_id, symbol):
    existing = Watchlist.query.filter_by(user_id=user_id, stock_symbol=symbol).first()
    if existing:
        return {"Message": "Action already in Watchlist", "Status": 409, "Result":"Ok"}
    
    item = Watchlist(user_id=user_id, stock_symbol=symbol)
    db.db.session.add(item)
    db.db.session.commit()
    return {"Message": f"Action {symbol} added to Watchlist", "Status": 201, "Result":"Ok"}

def view_watchlist(user_id):
    watchlist = Watchlist.query.filter_by(user_id=user_id).all()
    symbols = [item.stock_symbol for item in watchlist]
    
    result = []

    for symbol in symbols:
        try:
            price_response = stock_controller.td.price(symbol=symbol).as_json()
            if "price" in price_response:
                current_price = float(price_response["price"])
                result.append({
                    "symbol": symbol,
                    "price": current_price
                })
            else:
                result.append({
                    "symbol": symbol,
                    "error": "Sem preço"
                })
        except Exception as e:
            result.append({
                "symbol": symbol,
                "error": str(e)
            })

    return {
        "Message": "Watchlist fetched successfully",
        "Status": 200,
        "Result": result
    }
    
def remove_from_watchlist(user_id, symbol):
    existing = Watchlist.query.filter_by(user_id=user_id, stock_symbol=symbol).first()
    if existing:
        db.db.session.delete(existing)
        db.db.session.commit()
        return {
            "Message": f"Action {symbol} removed from Watchlist",
            "Status": 200,
            "Result": "Ok"
        }
    else:
        return {
            "Message": f"Action {symbol} not found in Watchlist",
            "Status": 404,
            "Result": "Error"
        }

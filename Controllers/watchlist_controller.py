from flask import Blueprint, request, jsonify
from Models import user_model as UserModel
from Models import watchlist_model as Watchlist
from Extras import db

def add_to_watchlist(user_id, symbol):
    existing = Watchlist.Watchlist.query.filter_by(user_id=user_id, stock_symbol=symbol).first()
    if existing:
        return {"Message": "Action already in Watchlist", "Status": 409, "Result":"Ok"}
    
    item = Watchlist.Watchlist(user_id=user_id, stock_symbol=symbol)
    db.db.session.add(item)
    db.db.session.commit()
    return {"Message": f"Action {symbol} added to Watchlist", "Status": 201, "Result":"Ok"}

def view_watchlist(user_id):
    watchlist = Watchlist.Watchlist.query.filter_by(user_id=user_id).all()
    symbols = [_.stock_symbol for _ in watchlist]

    return {
        "Message": "Watchlist fetched successfully",
        "Status": 200,
        "Result": symbols
    }
    
def remove_from_watchlist(user_id, symbol):
    existing = Watchlist.Watchlist.query.filter_by(user_id=user_id, stock_symbol=symbol).first()
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
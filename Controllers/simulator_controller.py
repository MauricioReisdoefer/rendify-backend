from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Extras.db import db
from Models.simulator_model import SimulatorModel
from Models.user_model import UserModel
from Controllers.stock_controller import get_stock

@jwt_required()
def add_or_update_simulator():
    user_id = get_jwt_identity()
    data = request.json
    symbol = data.get("symbol")
    exchange = data.get("exchange")
    currency = data.get("currency", "USD")
    ammount = data.get("ammount", 0)

    if not symbol or not exchange or not ammount:
        return jsonify({"error": "Symbol, exchange and positive ammount are required"}), 400

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    stock_response, status = get_stock(symbol)
    if status != 200:
        return jsonify({"error": "Stock not found"}), 404
    stock_data = stock_response.get_json()
    price = stock_data["price"]
    
    if user.balance < price * ammount:
        return jsonify({"invalid":"Not enough money"})

    sim = SimulatorModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if sim:
        sim.ammount += ammount
        sim.price = price
        sim.exchange = exchange
        sim.currency = currency
    else:
        sim = SimulatorModel(
            symbol=symbol,
            exchange=exchange,
            currency=currency,
            price=price,
            user=user,
            ammount=ammount
        )
        db.session.add(sim)
    
    user.balance -= price * ammount
    
    db.session.commit()
    return jsonify(sim.json()), 200

@jwt_required()
def get_simulator(symbol):
    user_id = get_jwt_identity()
    sim = SimulatorModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if not sim:
        return jsonify({"error": "Simulator item not found"}), 404
    return jsonify(sim.json()), 200

@jwt_required()
def get_all_simulators():
    user_id = get_jwt_identity()
    sims = SimulatorModel.query.filter_by(user_id=user_id).all()
    return jsonify([s.json() for s in sims]), 200

@jwt_required()
def delete_simulator(symbol):
    user_id = get_jwt_identity()
    sim = SimulatorModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if not sim:
        return jsonify({"error": "Simulator item not found"}), 404
    db.session.delete(sim)
    db.session.commit()
    return jsonify({"message": "Simulator item deleted successfully"}), 200

@jwt_required()
def sell_or_update_simulator():
    user_id = get_jwt_identity()
    data = request.json
    symbol = data.get("symbol")
    ammount = data.get("ammount", 0)

    if not symbol or ammount <= 0:
        return jsonify({"error": "Symbol and positive ammount are required"}), 400

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    sim = SimulatorModel.query.filter_by(user_id=user_id, symbol=symbol.upper()).first()
    if not sim:
        return jsonify({"error": "You don't own this stock"}), 400

    if sim.ammount < ammount:
        return jsonify({"invalid": "Not enough stock"}), 400

    stock_response, status = get_stock(symbol)
    if status != 200:
        return jsonify({"error": "Stock not found"}), 404
    stock_data = stock_response.get_json()
    price = stock_data["price"]

    sim.ammount -= ammount
    user.balance += price * ammount

    if sim.ammount == 0:
        db.session.delete(sim)

    db.session.commit()
    return jsonify({sim.json}), 200

@jwt_required()
def restart():
    user_id = get_jwt_identity()
    
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    SimulatorModel.query.filter_by(user_id=user_id).delete() 
    user.balance = 1000
    db.session.commit()
    return jsonify({"message": "Simulator reset successfully"}), 200
from flask import Blueprint, request, jsonify
from Controllers.simulator_stock_controller import (
    get_or_create_stock,
    get_all_stocks,
    buy_stock,
    sell_stock
)

sim_bp = Blueprint("simulator", __name__, url_prefix="/simulator")

@sim_bp.route("/stock/<string:symbol>", methods=["GET"])
def view_stock(symbol):
    return get_or_create_stock(symbol)

@sim_bp.route("/stocks", methods=["GET"])
def view_all_stocks():
    symbols = request.args.get("symbols", "")
    if not symbols:
        return jsonify({"Message": "Parâmetro 'symbols' é obrigatório", "Status": 400})
    return get_all_stocks(symbols)

@sim_bp.route("/buy", methods=["POST"])
def route_buy_stock():
    data = request.get_json()
    symbol = data.get("symbol")
    ammount = data.get("ammount")

    if not symbol or not ammount:
        return jsonify({"Message": "Campos 'symbol' e 'ammount' são obrigatórios", "Status": 400})

    return buy_stock(symbol, int(ammount))

@sim_bp.route("/sell", methods=["POST"])
def route_sell_stock():
    data = request.get_json()
    symbol = data.get("symbol")
    ammount = data.get("ammount")

    if not symbol or not ammount:
        return jsonify({"Message": "Campos 'symbol' e 'ammount' são obrigatórios", "Status": 400})

    return sell_stock(symbol, int(ammount))
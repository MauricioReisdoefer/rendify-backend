from flask import Blueprint
from Controllers.stock_controller import update_stock_price, get_stock

stock_bp = Blueprint("stock_bp", __name__, url_prefix="/stock")

stock_bp.route("/update", methods=["POST"])(update_stock_price)
stock_bp.route("/<string:symbol>", methods=["GET"])(get_stock)
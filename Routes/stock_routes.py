from flask import Blueprint
from Controllers.stock_controller import update_stock_price, get_stock, get_graphic, get_company

stock_bp = Blueprint("stock_bp", __name__, url_prefix="/stock")

stock_bp.route("/update", methods=["POST"])(update_stock_price)
stock_bp.route("/search/<string:symbol>", methods=["GET"])(get_stock)
stock_bp.route("/graph/<string:symbol>/<int:ammount>", methods=["GET"])(get_graphic)
stock_bp.route("/company/<string:symbol>")(get_company)
from flask import Blueprint
from Controllers.watchlist_controller import (
    add_or_update_watchlist,
    get_watchlist,
    get_all_watchlists,
    delete_watchlist,
)

watchlist_bp = Blueprint("watchlist_bp", __name__, url_prefix="/watchlist")

watchlist_bp.route("/add", methods=["POST"])(add_or_update_watchlist)
watchlist_bp.route("/<string:symbol>", methods=["GET"])(get_watchlist)
watchlist_bp.route("/", methods=["GET"])(get_all_watchlists) # Pega todas as ações da Watchlist
watchlist_bp.route("/<string:symbol>", methods=["DELETE"])(delete_watchlist)

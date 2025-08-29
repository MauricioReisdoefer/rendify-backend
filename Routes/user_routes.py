from flask import Blueprint
from Controllers.user_controller import register, login, view_me, update_me, delete_me

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")

# Rotas públicas
user_bp.route("/register", methods=["POST"])(register)
user_bp.route("/login", methods=["POST"])(login)

# Rotas protegidas por JWT
user_bp.route("/viewme", methods=["GET"])(view_me)
user_bp.route("/updateme", methods=["PUT"])(update_me)
user_bp.route("/deleteme", methods=["DELETE"])(delete_me)
from flask import Blueprint
from Controllers import user_controller

user_bp = Blueprint('/user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    return user_controller.register()

@user_bp.route('/login', methods=['POST'])
def login():
    return user_controller.login()

@user_bp.route('/change-password', methods=['POST'])
def change_pass():
    return user_controller.change_password()

@user_bp.route("/get_by_name/<name>")
def get_by_name(name):
    return user_controller.get_user_by_name(nome=name)

@user_bp.route("change_balance/", methods=['POST'])
def change_balance():
    return user_controller.change_balance()
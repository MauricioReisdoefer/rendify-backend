from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Extras.db import db
from Models.user_model import UserModel

def register():
    data = request.json
    if not data.get("name") or not data.get("password"):
        return jsonify({"error": "Name and password are required"}), 400

    existing_user = UserModel.query.filter_by(name=data["name"]).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    user = UserModel(name=data["name"], password=data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.json()), 201

def login():
    data = request.json
    if not data.get("name") or not data.get("password"):
        return jsonify({"error": "Name and password are required"}), 400

    user = UserModel.query.filter_by(name=data["name"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token})

@jwt_required()
def view_me(): # Mostra o usuário com a chave JWT que foi passada
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.json())

@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    if "name" in data:
        if UserModel.query.filter(UserModel.name == data["name"], UserModel.id != user_id).first():
            return jsonify({"error": "Name already taken"}), 409
        user.name = data["name"]

    if "password" in data:
        user.set_password(data["password"])

    if "balance" in data:
        try:
            user.balance = float(data["balance"])
        except ValueError:
            return jsonify({"error": "Balance must be a number"}), 400

    db.session.commit()
    return jsonify(user.json()), 200


@jwt_required()
def delete_me():
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
from flask import Blueprint, request, jsonify
from Models import user_model as UserModel
from Extras import db

def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    balance = data.get('balance', 2000.0)

    if not name or not password:
        return jsonify({"Message": "Name and password are required", "Status": 400, "Result": "Error"})

    if UserModel.User.query.filter_by(name=name).first():
        return jsonify({"Message": "User already exists", "Status": 409, "Result": "Error"})

    user = UserModel.User(name=name, balance=balance)
    user.change_password(password)
    db.db.session.add(user)
    db.db.session.commit()

    return jsonify({
        "Message": "User created",
        "Status": 201,
        "Result": {"id": user.id, "name": user.name, "balance": user.balance}
    })

def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    user = UserModel.User.query.filter_by(name=name).first()
    if not user:
        return jsonify({"Message": "User not found", "Status": 404, "Result": "Error"})

    result = user.check_password(password)
    return jsonify({"Message": "Password Correct", "Status": 200, "Result": "Ok"})

def change_password():
    data = request.get_json()
    name = data.get('name')
    new_password = data.get('new_password')

    user = UserModel.User.query.filter_by(name=name).first()
    if not user:
        return jsonify({"Message": "User not found", "Status": 404, "Result": "Error"}), 404

    result = user.change_password(new_password)
    db.db.session.commit()
    status = result["Status"]
    return jsonify(result), status

def get_user_by_name(nome):
    user = UserModel.User.query.filter_by(name=nome).first()
    
    if not user:
        return jsonify({"Message":"User Not Found", "Status":404, "Result":"Error"})
    
    return jsonify({
        "Message": "User Found",
        "Status": 200,
        "Result": {"id": user.id, "name": user.name, "balance": user.balance}
    })

def change_balance():
    data = request.get_json()
    id = data.get('id')
    new_balance = data.get('new_balance')

    user = UserModel.User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"Message": "User not found", "Status": 404, "Result": "Error"})

    result = user.change_balance(new_balance)
    if result["Status"] == 200:
        db.db.session.commit()

    return jsonify(result), result["Status"]

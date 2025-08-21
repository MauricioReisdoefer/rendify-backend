from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify
import werkzeug.security
from Extras import db

class User(db.db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True)
    name = db.db.Column(db.db.String(30), unique=True)
    password_hash = db.db.Column(db.db.String(128), nullable=True)
    balance = db.db.Column(db.db.Float, default=2000.0)
    
    def check_password(self, password_to_check:str): #  werkzeug.security.check_password_hash(self.password_hash, password_to_check)]
        if(password_to_check is None):
            return jsonify({"Message":"Password Cannot be Null", "Status":400, "Result":"Error"})
        return jsonify({"Message":"Password Suceffuly Changed", "Status":200, "Result":werkzeug.security.check_password_hash(self.password_hash, password_to_check)})
    
    def change_password(self, new_password:str):
        if(new_password != None):
            self.password_hash = werkzeug.security.generate_password_hash(new_password)
            return jsonify({"Message":"Password Suceffuly Changed", "Status":200, "Result":f"Password Changed to {new_password}"})
        else: return jsonify({"Message":"Password Cannot be Null", "Status":400, "Result":"Error"})

    def change_balance(self, new_balance: float):
        if new_balance is None:
            return {"Message": "Balance cannot be null", "Status": 400, "Result": "Error"}
        try:
            self.balance = float(new_balance)
            return {"Message": "Balance updated successfully", "Status": 200, "Result": {"balance": self.balance}}
        except ValueError:
            return {"Message": "Invalid value for balance", "Status": 400, "Result": "Error"}

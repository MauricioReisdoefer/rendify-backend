from Extras.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    
    watchlists = db.relationship("WatchlistModel", back_populates="user", cascade="all, delete")
    simulators = db.relationship("SimulatorModel", back_populates="user", cascade="all, delete")

    def __init__(self, name, password, balance=0.0):
        self.name = name
        self.set_password(password)
        self.balance = balance

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "balance": self.balance
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

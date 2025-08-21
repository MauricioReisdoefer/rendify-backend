from flask_sqlalchemy import SQLAlchemy
from Extras import db

class SimulatorStockModel(db.db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True)
    symbol = db.db.Column(db.db.String(30), unique=True)
    price = db.db.Column(db.db.Numeric(18, 8), nullable=False)
    ammount = db.db.Column(db.db.Integer)
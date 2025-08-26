from Extras.db import db
from datetime import datetime


class WatchlistModel(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("UserModel", back_populates="watchlists")

    def __init__(self, symbol, exchange, currency, price, user):
        self.symbol = symbol.upper()
        self.exchange = exchange
        self.currency = currency
        self.price = price
        self.user = user

    def json(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "exchange": self.exchange,
            "currency": self.currency,
            "price": self.price,
            "user_id": self.user_id,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

from Extras.db import db

class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stock_symbol = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, stock_symbol):
        self.user_id = user_id
        self.stock_symbol = stock_symbol
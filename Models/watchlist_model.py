from Extras import db

class Watchlist(db.db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True)
    stock_symbol = db.db.Column(db.db.String(10), nullable=False)  # "AAPL", "PETR4"
    user_id = db.db.Column(db.db.Integer, db.db.ForeignKey('user.id'), nullable=False)

    user = db.db.relationship('User', backref=db.db.backref('watchlist', lazy=True))
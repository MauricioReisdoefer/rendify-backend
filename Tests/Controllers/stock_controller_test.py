import pytest
from flask import Flask, json
from Extras.db import db
from Models.stock_model import StockModel
from Controllers.stock_controller import update_stock_price, get_stock

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

@pytest.fixture
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_update_and_get_stock(app, setup_db):
    with app.app_context():
        with app.test_request_context("/", method="POST", json={"symbol": "AAPL", "exchange": "NASDAQ"}):
            response, status = update_stock_price()
            assert status == 200
            data = json.loads(response.get_data(as_text=True))
            assert data["symbol"] == "AAPL"
            assert data["exchange"] == "NASDAQ"
            assert data["price"] > 0

        with app.test_request_context("/"):
            response, status = get_stock("AAPL") 
            assert status == 200
            data = json.loads(response.get_data(as_text=True))
            assert data["symbol"] == "AAPL"
            assert data["exchange"] == "NASDAQ"


def test_update_stock_existing(app, setup_db):
    with app.app_context():
        stock = StockModel(symbol="TSLA", exchange="NASDAQ", currency="USD", price=500)
        db.session.add(stock)
        db.session.commit()

        with app.test_request_context("/", method="POST", json={"symbol": "TSLA", "exchange": "NASDAQ"}):
            response, status = update_stock_price()
            assert status == 200
            data = json.loads(response.get_data(as_text=True))
            assert data["symbol"] == "TSLA"
            assert data["price"] != 500

import pytest
from flask import Flask
from Extras.db import db
from Models.stock_model import StockModel


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


def test_create_stock(session):
    stock = StockModel(symbol="AAPL", exchange="NASDAQ", currency="USD", price=170.5)
    stock.save_to_db()

    retrieved = session.query(StockModel).filter_by(symbol="AAPL").first()
    assert retrieved is not None
    assert retrieved.symbol == "AAPL"
    assert retrieved.exchange == "NASDAQ"
    assert retrieved.currency == "USD"
    assert retrieved.price == 170.5


def test_update_stock_price(session):
    stock = StockModel(symbol="TSLA", exchange="NASDAQ", currency="USD", price=700)
    stock.save_to_db()

    stock.price = 710
    stock.save_to_db()

    updated = session.query(StockModel).filter_by(symbol="TSLA").first()
    assert updated.price == 710


def test_delete_stock(session):
    stock = StockModel(symbol="GOOG", exchange="NASDAQ", currency="USD", price=2800)
    stock.save_to_db()

    stock.delete_from_db()
    deleted = session.query(StockModel).filter_by(symbol="GOOG").first()
    assert deleted is None


def test_json_method(session):
    stock = StockModel(symbol="MSFT", exchange="NASDAQ", currency="USD", price=330)
    stock.save_to_db()

    data = stock.json()
    assert data["symbol"] == "MSFT"
    assert data["exchange"] == "NASDAQ"
    assert data["currency"] == "USD"
    assert data["price"] == 330
    assert "updated_at" in data

import pytest
from flask import Flask
from Extras.db import db
from Routes.stock_routes import stock_bp
from Models.stock_model import StockModel


@pytest.fixture
def app(monkeypatch):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(stock_bp)

    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()

class MockPrice:
    def __init__(self, price):
        self._price = price

    def as_json(self):
        return {"price": str(self._price)}


def test_update_stock_new(client, monkeypatch):
    monkeypatch.setattr("Controllers.stock_controller.td.price", lambda symbol: MockPrice(150.5))

    response = client.post("/stock/update", json={
        "symbol": "AAPL",
        "exchange": "NASDAQ",
        "currency": "USD"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["symbol"] == "AAPL"
    assert data["exchange"] == "NASDAQ"
    assert float(data["price"]) == 150.5


def test_update_stock_existing(client, monkeypatch):
    monkeypatch.setattr("Controllers.stock_controller.td.price", lambda symbol: MockPrice(100.0))
    client.post("/stock/update", json={"symbol": "AAPL", "exchange": "NASDAQ"})

    monkeypatch.setattr("Controllers.stock_controller.td.price", lambda symbol: MockPrice(200.0))
    response = client.post("/stock/update", json={"symbol": "AAPL", "exchange": "NASDAQ"})

    assert response.status_code == 200
    data = response.get_json()
    assert float(data["price"]) == 200.0 


def test_update_stock_missing_fields(client):
    response = client.post("/stock/update", json={"symbol": "AAPL"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_stock_found(client, monkeypatch):
    monkeypatch.setattr("Controllers.stock_controller.td.price", lambda symbol: MockPrice(50.0))
    client.post("/stock/update", json={"symbol": "TSLA", "exchange": "NASDAQ"})

    res = client.get("/stock/TSLA")
    assert res.status_code == 200
    assert res.get_json()["symbol"] == "TSLA"


def test_get_stock_not_found(client):
    res = client.get("/stock/INVALID")
    assert res.status_code == 404
    assert "error" in res.get_json()

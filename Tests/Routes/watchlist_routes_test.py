import pytest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from Extras.db import db
from Routes.watchlist_routes import watchlist_bp
from Models.user_model import UserModel
from Models.watchlist_model import WatchlistModel


@pytest.fixture
def app(monkeypatch):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "qlqr-coisa"

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(watchlist_bp)

    with app.app_context():
        db.create_all()
        user = UserModel(name="tester", password="123")
        db.session.add(user)
        db.session.commit()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_header(app):
    """Gera token JWT para o usuário de teste"""
    with app.app_context():
        user = UserModel.query.filter_by(name="tester").first()
        token = create_access_token(identity=str(user.id))
    return {"Authorization": f"Bearer {token}"}

def mock_get_stock_ok(symbol):
    return jsonify({"symbol": symbol.upper(), "price": 99.9, "exchange": "NASDAQ", "currency": "USD"}), 200


def mock_get_stock_not_found(symbol):
    return jsonify({"error": "Stock not found"}), 404


def test_add_watchlist_new(client, auth_header, monkeypatch):
    monkeypatch.setattr("Controllers.watchlist_controller.get_stock", mock_get_stock_ok)

    res = client.post("/watchlist/add", json={"symbol": "AAPL", "exchange": "NASDAQ"}, headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()
    assert data["symbol"] == "AAPL"
    assert float(data["price"]) == 99.9


def test_add_watchlist_existing(client, auth_header, monkeypatch):
    monkeypatch.setattr("Controllers.watchlist_controller.get_stock", mock_get_stock_ok)
    
    client.post("/watchlist/add", json={"symbol": "AAPL", "exchange": "NASDAQ"}, headers=auth_header)
    res = client.post("/watchlist/add", json={"symbol": "AAPL", "exchange": "NYSE"}, headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["exchange"] == "NYSE"


def test_add_watchlist_stock_not_found(client, auth_header, monkeypatch):
    monkeypatch.setattr("Controllers.watchlist_controller.get_stock", mock_get_stock_not_found)

    res = client.post("/watchlist/add", json={"symbol": "INVALID", "exchange": "NYSE"}, headers=auth_header)
    assert res.status_code == 404
    assert "error" in res.get_json()


def test_get_watchlist(client, auth_header, monkeypatch):
    monkeypatch.setattr("Controllers.watchlist_controller.get_stock", mock_get_stock_ok)

    client.post("/watchlist/add", json={"symbol": "TSLA", "exchange": "NASDAQ"}, headers=auth_header)
    res = client.get("/watchlist/TSLA", headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["symbol"] == "TSLA"


def test_get_watchlist_not_found(client, auth_header):
    res = client.get("/watchlist/NONE", headers=auth_header)
    assert res.status_code == 404
    assert "error" in res.get_json()


def test_get_all_watchlists(client, auth_header, monkeypatch):
    monkeypatch.setattr("Controllers.watchlist_controller.get_stock", mock_get_stock_ok)

    client.post("/watchlist/add", json={"symbol": "AAPL", "exchange": "NASDAQ"}, headers=auth_header)
    client.post("/watchlist/add", json={"symbol": "TSLA", "exchange": "NASDAQ"}, headers=auth_header)

    res = client.get("/watchlist/", headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
    assert {item["symbol"] for item in data} == {"AAPL", "TSLA"}


def test_delete_watchlist(client, auth_header, monkeypatch):
    monkeypatch.setattr("Controllers.watchlist_controller.get_stock", mock_get_stock_ok)

    client.post("/watchlist/add", json={"symbol": "AAPL", "exchange": "NASDAQ"}, headers=auth_header)
    res = client.delete("/watchlist/AAPL", headers=auth_header)

    assert res.status_code == 200
    assert res.get_json()["message"] == "Watchlist item deleted successfully"


def test_delete_watchlist_not_found(client, auth_header):
    res = client.delete("/watchlist/INVALID", headers=auth_header)
    assert res.status_code == 404
    assert "error" in res.get_json()

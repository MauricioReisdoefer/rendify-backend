import pytest
from flask import Flask, json
from flask_jwt_extended import JWTManager, create_access_token
from Extras.db import db
from Models.user_model import UserModel
from Models.watchlist_model import WatchlistModel
from Controllers.watchlist_controller import (
    add_or_update_watchlist,
    get_watchlist,
    get_all_watchlists,
    delete_watchlist
)
from Controllers.stock_controller import StockModel

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
    db.init_app(app)
    JWTManager(app)
    return app

@pytest.fixture
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user_token(app, setup_db):
    with app.app_context():
        user = UserModel(name="tester", password="1234")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id))
        return user, token

def test_watchlist_crud(app, setup_db, user_token):
    user, token = user_token
    headers = {"Authorization": f"Bearer {token}"}

    with app.app_context():
        stock = StockModel(symbol="AAPL", exchange="NASDAQ", currency="USD", price=150)
        db.session.add(stock)
        db.session.commit()
        
        with app.test_request_context("/", method="POST", json={"symbol": "AAPL", "exchange": "NASDAQ"}, headers=headers):
            response, status = add_or_update_watchlist()
            data = json.loads(response.get_data(as_text=True))
            assert status == 200
            assert data["symbol"] == "AAPL"
            assert data["exchange"] == "NASDAQ"

        with app.test_request_context("/", method="GET", headers=headers):
            response, status = get_watchlist("AAPL")
            data = json.loads(response.get_data(as_text=True))
            assert status == 200
            assert data["symbol"] == "AAPL"

        with app.test_request_context("/", method="GET", headers=headers):
            response, status = get_all_watchlists()
            data = json.loads(response.get_data(as_text=True))
            assert status == 200
            assert len(data) == 1
            assert data[0]["symbol"] == "AAPL"

        with app.test_request_context("/", method="DELETE", headers=headers):
            response, status = delete_watchlist("AAPL")
            data = json.loads(response.get_data(as_text=True))
            assert status == 200
            assert data["message"] == "Watchlist item deleted successfully"

        with app.test_request_context("/", method="GET", headers=headers):
            response, status = get_watchlist("AAPL")
            assert status == 404

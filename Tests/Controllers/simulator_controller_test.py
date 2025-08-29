import pytest
from flask import Flask, json
from flask_jwt_extended import JWTManager, create_access_token
from Extras.db import db
from Models.user_model import UserModel
from Models.simulator_model import SimulatorModel
from Controllers.simulator_controller import (
    add_or_update_simulator,
    get_simulator,
    get_all_simulators,
    delete_simulator
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

def test_simulator_crud(app, setup_db, user_token):
    user, token = user_token
    headers = {"Authorization": f"Bearer {token}"}

    with app.app_context():
        stock = StockModel(symbol="AAPL", exchange="NASDAQ", currency="USD", price=150)
        db.session.add(stock)
        db.session.commit()

        with app.test_request_context("/", method="POST",
                                      json={"symbol": "AAPL", "exchange": "NASDAQ", "ammount": 10},
                                      headers=headers):
            response, status = add_or_update_simulator()
            data = response.get_json()
            assert status == 200
            assert data["symbol"] == "AAPL"
            assert data["exchange"] == "NASDAQ"
            assert data["ammount"] == 10

        with app.test_request_context("/", method="POST",
                                      json={"symbol": "AAPL", "exchange": "NASDAQ", "ammount": 5},
                                      headers=headers):
            response, status = add_or_update_simulator()
            data = response.get_json()
            assert status == 200
            assert data["ammount"] == 15  

        with app.test_request_context("/", method="GET", headers=headers):
            response, status = get_simulator("AAPL")
            data = response.get_json()
            assert status == 200
            assert data["symbol"] == "AAPL"

        with app.test_request_context("/", method="GET", headers=headers):
            response, status = get_all_simulators()
            data = response.get_json()
            assert status == 200
            assert len(data) == 1
            assert data[0]["symbol"] == "AAPL"

        with app.test_request_context("/", method="DELETE", headers=headers):
            response, status = delete_simulator("AAPL")
            data = response.get_json()
            assert status == 200
            assert data["message"] == "Simulator item deleted successfully"

        with app.test_request_context("/", method="GET", headers=headers):
            response, status = get_simulator("AAPL")
            assert status == 404
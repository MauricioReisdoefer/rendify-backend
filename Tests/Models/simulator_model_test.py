import pytest
from datetime import datetime
from flask import Flask
from Extras.db import db
from Models.simulator_model import SimulatorModel
from Models.user_model import UserModel

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


@pytest.fixture
def user(setup_db):
    u = UserModel(name="teste", password="1234")
    setup_db.session.add(u)
    setup_db.session.commit()
    return u



def test_create_simulator(setup_db, user):
    sim = SimulatorModel("AAPL", "NASDAQ", "USD", 190.5, user, 10)
    sim.save_to_db()

    db_sim = SimulatorModel.query.first()
    assert db_sim is not None
    assert db_sim.symbol == "AAPL"
    assert db_sim.exchange == "NASDAQ"
    assert db_sim.currency == "USD"
    assert db_sim.price == 190.5
    assert db_sim.ammount == 10
    assert db_sim.user_id == user.id


def test_json_method(setup_db, user):
    sim = SimulatorModel("TSLA", "NASDAQ", "USD", 240.0, user, 5)
    sim.save_to_db()

    data = sim.json()
    assert data["symbol"] == "TSLA"
    assert data["exchange"] == "NASDAQ"
    assert data["currency"] == "USD"
    assert data["price"] == 240.0
    assert data["ammount"] == 5
    assert data["user_id"] == user.id
    assert "updated_at" in data


def test_delete_simulator(setup_db, user):
    sim = SimulatorModel("MSFT", "NASDAQ", "USD", 300.0, user, 3)
    sim.save_to_db()

    sim_id = sim.id
    sim.delete_from_db()

    db_sim = SimulatorModel.query.get(sim_id)
    assert db_sim is None

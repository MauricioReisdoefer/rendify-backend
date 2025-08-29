import pytest
from flask import Flask
from Extras.db import db
from Models.user_model import UserModel
from Models.watchlist_model import WatchlistModel
from Models.simulator_model import SimulatorModel

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


def test_create_user(session):
    user = UserModel(name="Maurício", password="123456", balance=100.0)
    user.save_to_db()

    retrieved = session.query(UserModel).filter_by(name="Maurício").first()
    assert retrieved is not None
    assert retrieved.name == "Maurício"
    assert retrieved.balance == 100.0
    assert retrieved.password_hash != "123456"


def test_check_password(session):
    user = UserModel(name="Teste", password="senha123")
    user.save_to_db()

    retrieved = session.query(UserModel).filter_by(name="Teste").first()
    assert retrieved.check_password("senha123") is True
    assert retrieved.check_password("errada") is False


def test_update_balance(session):
    user = UserModel(name="Saldo", password="abc", balance=50.0)
    user.save_to_db()

    user.balance += 25
    user.save_to_db()

    updated = session.query(UserModel).filter_by(name="Saldo").first()
    assert updated.balance == 75.0


def test_delete_user(session):
    user = UserModel(name="Delete", password="123")
    user.save_to_db()

    user.delete_from_db()
    deleted = session.query(UserModel).filter_by(name="Delete").first()
    assert deleted is None


def test_json_method(session):
    user = UserModel(name="JsonTest", password="xyz", balance=200)
    user.save_to_db()

    data = user.json()
    assert data["name"] == "JsonTest"
    assert data["balance"] == 200
    assert "id" in data
    assert "password_hash" not in data  
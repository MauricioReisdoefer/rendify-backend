import pytest
from flask import Flask
from Extras.db import db
from Models.user_model import UserModel
from Models.watchlist_model import WatchlistModel


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


def test_create_watchlist_entry(session):
    user = UserModel(name="Maurício", password="123456")
    user.save_to_db()

    entry = WatchlistModel(symbol="AAPL", exchange="NASDAQ", currency="USD", price=170, user=user)
    entry.save_to_db()

    retrieved = session.query(WatchlistModel).filter_by(symbol="AAPL").first()
    assert retrieved is not None
    assert retrieved.symbol == "AAPL"
    assert retrieved.user.id == user.id
    assert retrieved.user.name == "Maurício"


def test_update_watchlist_price(session):
    user = UserModel(name="Teste", password="senha123")
    user.save_to_db()

    entry = WatchlistModel(symbol="TSLA", exchange="NASDAQ", currency="USD", price=700, user=user)
    entry.save_to_db()

    # Atualiza o preço
    entry.price = 710
    entry.save_to_db()

    updated = session.query(WatchlistModel).filter_by(symbol="TSLA").first()
    assert updated.price == 710


def test_delete_watchlist_entry(session):
    user = UserModel(name="DeleteUser", password="123")
    user.save_to_db()

    entry = WatchlistModel(symbol="GOOG", exchange="NASDAQ", currency="USD", price=2800, user=user)
    entry.save_to_db()

    entry.delete_from_db()
    deleted = session.query(WatchlistModel).filter_by(symbol="GOOG").first()
    assert deleted is None


def test_json_method(session):
    user = UserModel(name="JsonUser", password="xyz")
    user.save_to_db()

    entry = WatchlistModel(symbol="MSFT", exchange="NASDAQ", currency="USD", price=330, user=user)
    entry.save_to_db()

    data = entry.json()
    assert data["symbol"] == "MSFT"
    assert data["user_id"] == user.id
    assert data["price"] == 330
    assert "updated_at" in data

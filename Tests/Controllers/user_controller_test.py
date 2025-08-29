import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from Extras.db import db
from Models.user_model import UserModel
from Controllers.user_controller import register, login, view_me, update_me, delete_me

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

def test_register_login_view(app, setup_db):
    with app.app_context():
        # Register
        with app.test_request_context(json={"name": "teste", "password": "1234"}):
            resp, code = register()
            assert code == 201
            data = resp.get_json()
            assert data["name"] == "teste"
            assert data["balance"] == 0.0

        # Login
        with app.test_request_context(json={"name": "teste", "password": "1234"}):
            resp = login()
            data = resp.get_json()
            token = data["access_token"]
            assert token is not None

        # View_me
        headers = {"Authorization": f"Bearer {token}"}
        with app.test_request_context(headers=headers):
            resp = view_me()
            data = resp.get_json()
            assert data["name"] == "teste"

def test_update_delete_me(app, setup_db):
    with app.app_context():
        # Criar usuário
        with app.test_request_context(json={"name": "teste2", "password": "1234"}):
            register()

        # Login
        with app.test_request_context(json={"name": "teste2", "password": "1234"}):
            resp = login()
            token = resp.get_json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # Update_me
        with app.test_request_context(json={"name": "novoNome", "balance": 100}, headers=headers):
            resp, code = update_me()
            assert code == 200
            data = resp.get_json()
            assert data["name"] == "novoNome"
            assert data["balance"] == 100

        # Delete_me
        with app.test_request_context(headers=headers):
            resp, code = delete_me()
            assert code == 200
            assert resp.get_json()["message"] == "User deleted successfully"

        # Confirma remoção
        with app.test_request_context(headers=headers):
            resp = view_me()
            assert resp[1] == 404
import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from Extras.db import db
from Routes.user_routes import user_bp
from Models.user_model import UserModel

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-secret"

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_success(client):
    response = client.post("/user/register", json={"name": "testuser", "password": "123"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "testuser"


def test_register_duplicate(client):
    client.post("/user/register", json={"name": "testuser", "password": "123"})
    response = client.post("/user/register", json={"name": "testuser", "password": "123"})
    assert response.status_code == 409


def test_login_success(client):
    client.post("/user/register", json={"name": "testuser", "password": "123"})
    response = client.post("/user/login", json={"name": "testuser", "password": "123"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_invalid(client):
    response = client.post("/user/login", json={"name": "invalid", "password": "wrong"})
    assert response.status_code == 401


def test_view_me(client):
    client.post("/user/register", json={"name": "testuser", "password": "123"})
    login_res = client.post("/user/login", json={"name": "testuser", "password": "123"})
    token = login_res.get_json()["access_token"]

    res = client.get("/user/viewme", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.get_json()["name"] == "testuser"


def test_update_me(client):
    client.post("/user/register", json={"name": "testuser", "password": "123"})
    login_res = client.post("/user/login", json={"name": "testuser", "password": "123"})
    token = login_res.get_json()["access_token"]

    res = client.put(
        "/user/updateme",
        json={"name": "newname"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.get_json()["name"] == "newname"


def test_delete_me(client):
    client.post("/user/register", json={"name": "testuser", "password": "123"})
    login_res = client.post("/user/login", json={"name": "testuser", "password": "123"})
    token = login_res.get_json()["access_token"]

    res = client.delete("/user/deleteme", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.get_json()["message"] == "User deleted successfully"
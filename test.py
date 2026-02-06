import pytest
from unittest.mock import MagicMock
import app as flask_app
from botocore.exceptions import ClientError

# MOCK AWS SERVICES PROPERLY

@pytest.fixture(autouse=True)
def mock_aws_services():
    flask_app.users_table = MagicMock()
    flask_app.admin_table = MagicMock()
    flask_app.sns = MagicMock()
    flask_app.dynamodb = MagicMock()

    yield

# FLASK TEST CLIENT

@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    flask_app.app.config["SECRET_KEY"] = "test-secret"

    with flask_app.app.test_client() as client:
        yield client

# BASIC PAGE TESTS

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_about_page(client):
    response = client.get("/aboutus")
    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200

# SIGNUP LOGIC TEST

def test_signup_success(client):
    flask_app.users_table.put_item.return_value = {}

    response = client.post("/signup", data={
        "name": "Test User",
        "email": "test@gmail.com",
        "password": "123456"
    }, follow_redirects=True)

    assert response.status_code == 200
    flask_app.users_table.put_item.assert_called_once()
    flask_app.sns.publish.assert_called_once()

# LOGIN LOGIC TEST

def test_login_success(client):
    flask_app.users_table.get_item.return_value = {
        "Item": {
            "email": "test@gmail.com",
            "name": "Test User",
            "password": flask_app.generate_password_hash("123456")
        }
    }

    response = client.post("/login", data={
        "email": "test@gmail.com",
        "password": "123456"
    }, follow_redirects=True)

    assert response.status_code == 200


def test_login_invalid_user(client):
    flask_app.users_table.get_item.return_value = {}

    response = client.post("/login", data={
        "email": "wrong@gmail.com",
        "password": "wrong"
    })

    assert response.status_code == 302

# ADMIN AUTH TESTS

def test_admin_dashboard_redirect(client):
    response = client.get("/admin-dashboard")
    assert response.status_code in [301, 302]


def test_admin_dashboard_with_session(client):
    with client.session_transaction() as session:
        session["admin"] = "admin"

    response = client.get("/admin-dashboard")
    assert response.status_code == 200

# USERS LIST TEST

def test_get_users(client):
    flask_app.users_table.scan.return_value = {
        "Items": [{"email": "test@gmail.com"}]
    }

    with client.session_transaction() as session:
        session["admin"] = "admin"

    response = client.get("/admin/get-users")
    assert response.status_code == 200

# LOGOUT TEST

def test_logout(client):
    with client.session_transaction() as session:
        session["user_id"] = "test@gmail.com"

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200

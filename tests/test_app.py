import os

import pytest

from app import app


@pytest.fixture
def client(tmp_path):
    app.config.update(TESTING=True, DATABASE=str(tmp_path / "test.db"), SECRET_KEY="test")
    with app.test_client() as client:
        yield client


def register(client):
    response = client.post("/register", data={"name": "Asha Rao", "email": "asha@example.com", "password": "password123"}, follow_redirects=True)
    client.post("/login", data={"email": "asha@example.com", "password": "password123"})
    return response


def test_register_login_and_dashboard(client):
    response = register(client)
    assert response.status_code == 200
    response = client.post("/login", data={"email": "asha@example.com", "password": "password123"}, follow_redirects=True)
    assert b"Good to see you" in response.data


def test_transaction_validation_and_persistence(client):
    register(client)
    response = client.post("/transactions/new", data={"type": "EXPENSE", "amount": "-2", "description": "Bad"}, follow_redirects=True)
    assert b"Check the transaction" in response.data
    response = client.post("/transactions/new", data={"type": "EXPENSE", "amount": "250.50", "description": "Groceries", "transaction_date": "2026-08-24", "payment_method": "UPI"}, follow_redirects=True)
    assert b"Groceries" in response.data


def test_private_routes_redirect(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

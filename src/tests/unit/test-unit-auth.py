import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from jose import jwt
from datetime import timedelta, datetime

from app.auth import (
    create_access_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM,
)

app = FastAPI()


@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {"email": user["email"], "role": user["role"]}


client = TestClient(app)


def test_creer_token_valide():
    data = {"sub": "user@example.com", "role": "ADMIN"}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "user@example.com"
    assert decoded["role"] == "ADMIN"
    assert "exp" in decoded


def test_valider_token_valide():
    token = create_access_token({"sub": "user@example.com", "role": "USER"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"email": "user@example.com", "role": "USER"}


def test_valider_token_manquant():
    # Aucun token initialisé et passé en header
    response = client.get("/protected")
    assert response.status_code == 403


def test_token_signature_invalide():
    mauvais_token = jwt.encode(
        {"sub": "user@example.com", "role": "USER"}, "ItemAdditionnel", algorithm=ALGORITHM)
    headers = {"Authorization": f"Bearer {mauvais_token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert "invalide" in response.json()["detail"]


def test_token_expire():
    expiration_passee = datetime.utcnow() - timedelta(minutes=1)
    token_expire = jwt.encode(
        {"sub": "user@example.com", "role": "USER", "exp": expiration_passee},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    headers = {"Authorization": f"Bearer {token_expire}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401

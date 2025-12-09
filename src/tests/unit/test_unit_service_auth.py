import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
from jose import jwt
from auth.services.services_auth import *
from auth.interface.model_view.model_view_token import TokenView
from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded
from auth.interface.model_view.model_view_refresh_token_decoded import RefreshTokenViewDecoded
from auth.data.dao.dao_auth import TokenDatabaseError
from auth.config.env import settings


def test_issue_token_succes(monkeypatch):
    mockDAO = Mock() 
    service = TokenServices(mockDAO)

    monkeypatch.setattr(service, "create_access_token", lambda user_data: "ACCESS_TOKEN")
    monkeypatch.setattr(service, "create_refresh_token", lambda user_data: "REFRESH_TOKEN")

    user_data = {"sub": "user@example.com", "id": 1, "role": "USER"}

    result = service.issue_token(user_data)

    assert isinstance(result, TokenView)
    assert result.access_token == "ACCESS_TOKEN"
    assert result.refresh_token == "REFRESH_TOKEN"


def test_create_access_token_succes(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    captured_payload = {}

    def fake_encode(payload, secret, algorithm):
        captured_payload["payload"] = payload
        captured_payload["secret"] = secret
        captured_payload["algorithm"] = algorithm
        return "ENCODED_ACCESS_TOKEN"

    monkeypatch.setattr(jwt, "encode", fake_encode)

    user_data = {"sub": "user@example.com", "id": 1, "role": "USER"}

    token = service.create_access_token(user_data)

    assert token == "ENCODED_ACCESS_TOKEN"
    assert captured_payload["payload"]["sub"] == "user@example.com"
    assert captured_payload["payload"]["id"] == 1
    assert captured_payload["payload"]["role"] == "USER"
    assert "exp" in captured_payload["payload"]
    assert captured_payload["secret"] == settings.JWT_SECRET
    assert captured_payload["algorithm"] == settings.JWT_ALGORITHM


def test_create_access_token_erreur_encode(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    def fake_encode(*args, **kwargs):
        raise Exception("encode error")

    monkeypatch.setattr(jwt, "encode", fake_encode)

    with pytest.raises(HTTPException) as exc_info:
        service.create_access_token({"sub": "user@example.com"})

    assert exc_info.value.status_code == 500
    assert "creation du token d'access" in exc_info.value.detail


def test_create_refresh_token_succes(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    captured_payload = {}
    captured_db_data = {}

    def fake_encode(payload, secret, algorithm):
        captured_payload["payload"] = payload
        captured_payload["secret"] = secret
        captured_payload["algorithm"] = algorithm
        return "ENCODED_REFRESH_TOKEN"

    monkeypatch.setattr(jwt, "encode", fake_encode)

    def fake_save_refresh_token(token_data):
        captured_db_data["data"] = token_data

    mockDAO.save_refresh_token.side_effect = fake_save_refresh_token

    user_data = {"sub": "user@example.com"}

    token = service.create_refresh_token(user_data)

    assert token == "ENCODED_REFRESH_TOKEN"
    assert captured_payload["payload"]["sub"] == "user@example.com"
    assert "jwt_id" in captured_payload["payload"]
    assert "exp" in captured_payload["payload"]
    assert captured_payload["secret"] == settings.REFRESH_JWT_SECRET
    assert captured_payload["algorithm"] == settings.JWT_ALGORITHM
    assert captured_db_data["data"]["sub"] == "user@example.com"
    assert "jwt_id" in captured_db_data["data"]
    assert "exp" in captured_db_data["data"]

    mockDAO.save_refresh_token.assert_called_once()


def test_create_refresh_token_erreur_database(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)
    monkeypatch.setattr(jwt, "encode", lambda *args, **kwargs: "TOKEN")
    mockDAO.save_refresh_token.side_effect = TokenDatabaseError("DB error")

    with pytest.raises(HTTPException) as exc_info:
        service.create_refresh_token({"sub": "user@example.com"})

    assert exc_info.value.status_code == 500
    assert "sauvegarde du token de rafraichissement" in exc_info.value.detail


def test_create_refresh_token_erreur_generale(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    monkeypatch.setattr(jwt, "encode", lambda *args, **kwargs: "TOKEN")

    mockDAO.save_refresh_token.side_effect = Exception("autre erreur")

    with pytest.raises(HTTPException) as exc_info:
        service.create_refresh_token({"sub": "user@example.com"})

    assert exc_info.value.status_code == 500
    assert "creation du token de rafraichissement" in exc_info.value.detail


def test_refresh_access_token_succes(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    refresh_payload = {
        "jwt_id": "1234",
        "sub": "user@example.com",
        "exp": 9999999999,
    }
    access_payload = {
        "sub": "user@example.com",
        "id": 1,
        "role": "USER",
        "exp": 9999999999,
    }

    def fake_decode(token, secret, algorithms, options=None):
        if secret == settings.REFRESH_JWT_SECRET:
            return refresh_payload
        elif secret == settings.JWT_SECRET:
            return access_payload
        else:
            raise InvalidTokenError("bad secret")

    monkeypatch.setattr(jwt, "decode", fake_decode)
    monkeypatch.setattr(service, "create_access_token", lambda user_data: "NEW_ACCESS")
    monkeypatch.setattr(service, "create_refresh_token", lambda user_data: "NEW_REFRESH")

    refresh_token = "OLD_REFRESH"
    old_access_token = "OLD_ACCESS"

    result = service.refresh_access_token(refresh_token, old_access_token)

    assert isinstance(result, TokenView)
    assert result.access_token == "NEW_ACCESS"
    assert result.refresh_token == "NEW_REFRESH"
    mockDAO.update_refresh_token_state.assert_called_once_with("1234", True)


def test_refresh_access_token_refresh_expire(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    def fake_decode_refresh(token, secret, algorithms, options=None):
        if secret == settings.REFRESH_JWT_SECRET:
            raise ExpiredSignatureError("expired")
        return {}

    monkeypatch.setattr(jwt, "decode", fake_decode_refresh)

    with pytest.raises(HTTPException) as exc_info:
        service.refresh_access_token("REFRESH", "ACCESS")

    assert exc_info.value.status_code == 401
    assert "rafraichissement expire" in exc_info.value.detail


def test_refresh_access_token_refresh_invalide(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    def fake_decode_refresh(token, secret, algorithms, options=None):
        if secret == settings.REFRESH_JWT_SECRET:
            raise InvalidTokenError("invalid")
        return {}

    monkeypatch.setattr(jwt, "decode", fake_decode_refresh)

    with pytest.raises(HTTPException) as exc_info:
        service.refresh_access_token("REFRESH", "ACCESS")

    assert exc_info.value.status_code == 401
    assert "rafraichissement invalide" in exc_info.value.detail


def test_refresh_access_token_access_invalide(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    refresh_payload = {
        "jwt_id": "1234",
        "sub": "user@example.com",
        "exp": 9999999999,
    }

    def fake_decode(token, secret, algorithms, options=None):
        if secret == settings.REFRESH_JWT_SECRET:
            return refresh_payload
        elif secret == settings.JWT_SECRET:
            raise DecodeError("bad access")
        else:
            raise InvalidTokenError("bad")

    monkeypatch.setattr(jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        service.refresh_access_token("REFRESH", "ACCESS")

    assert exc_info.value.status_code == 401
    assert "Token d'access invalide" in exc_info.value.detail


def test_refresh_access_token_erreur_database_invalidation(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    refresh_payload = {
        "jwt_id": "1234",
        "sub": "user@example.com",
        "exp": 9999999999,
    }
    access_payload = {
        "sub": "user@example.com",
        "id": 1,
        "role": "USER",
        "exp": 9999999999,
    }

    def fake_decode(token, secret, algorithms, options=None):
        if secret == settings.REFRESH_JWT_SECRET:
            return refresh_payload
        elif secret == settings.JWT_SECRET:
            return access_payload
        else:
            raise InvalidTokenError("bad secret")

    monkeypatch.setattr(jwt, "decode", fake_decode)

    mockDAO.update_refresh_token_state.side_effect = TokenDatabaseError("DB error")

    with pytest.raises(HTTPException) as exc_info:
        service.refresh_access_token("REFRESH", "ACCESS")

    assert exc_info.value.status_code == 500
    assert "invalidation du token de rafraichissement" in exc_info.value.detail


def test_validate_token_succes(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    payload = {
        "sub": "user@example.com",
        "id": 1,
        "role": "USER",
        "exp": 9999999999,
    }

    def fake_decode(token, secret, algorithms):
        return payload

    monkeypatch.setattr(jwt, "decode", fake_decode)

    result = service.validate_token("TOKEN")

    assert isinstance(result, TokenViewDecoded)
    assert result.sub == "user@example.com"
    assert result.id == 1
    assert result.role == "USER"


def test_validate_token_expire(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    def fake_decode(token, secret, algorithms):
        raise ExpiredSignatureError("expired")

    monkeypatch.setattr(jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        service.validate_token("TOKEN")

    assert exc_info.value.status_code == 403
    assert "Token expire" in exc_info.value.detail


def test_validate_token_invalide(monkeypatch):
    mockDAO = Mock()
    service = TokenServices(mockDAO)

    def fake_decode(token, secret, algorithms):
        raise InvalidTokenError("invalid")

    monkeypatch.setattr(jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        service.validate_token("TOKEN")

    assert exc_info.value.status_code == 401
    assert "invalide" in exc_info.value.detail
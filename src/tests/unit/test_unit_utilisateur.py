import pytest
from pydantic import ValidationError
from services.service_utilisateurs import UserServices
from data.models.model_utilisateur import UtilisateurModify


class FakeCursor:
    def __init__(self, rowcount=1):
        self.rowcount = rowcount
        self.last_query = None
        self.last_values = None
        self.closed = False

    def execute(self, query, values):
        self.last_query = query
        self.last_values = values

    def close(self):
        self.closed = True

class FakeDB:
    def __init__(self, cursor: FakeCursor):
        self._cursor = cursor
        self.commit_called = False

    def cursor(self, dictionary=True):
        return self._cursor

    def commit(self):
        self.commit_called = True




#test changement de status
def test_update_user_status_succes():
    cursor = FakeCursor()
    fake_db = FakeDB(cursor)
    service = UserServices(fake_db)
    expected_user = {"id": 2, "status_actif": True}
    called_with_id = {}
    def fake_get_user(user_id: int):
        called_with_id["id"] = user_id
        return expected_user
    service.get_utilisateur_by_id = fake_get_user
    result = service.update_user_status(2, True)
    assert cursor.last_query == (
        "UPDATE utilisateur SET status_actif = %s WHERE utilisateur_id = %s"
    )
    assert cursor.last_values == [True, 2]
    assert fake_db.commit_called is True
    assert called_with_id["id"] == 2
    assert result == expected_user

def test_update_user_status_utilisateur_non_trouve():
    cursor = FakeCursor()
    fake_db = FakeDB(cursor)
    service = UserServices(fake_db)
    called_with_id = {}
    def fake_get_user(user_id: int):
        called_with_id["id"] = user_id
        return None  

    service.get_utilisateur_by_id = fake_get_user
    result = service.update_user_status(99, True)
    
    assert cursor.last_query == (
        "UPDATE utilisateur SET status_actif = %s WHERE utilisateur_id = %s"
    )
    assert cursor.last_values == [True, 99]
    assert fake_db.commit_called is True
    assert called_with_id["id"] == 99
    assert result is None


#test modification utilisateur
def test_edit_user_succes():
    cursor = FakeCursor()
    fake_db = FakeDB(cursor)
    service = UserServices(fake_db)

    data = UtilisateurModify(
        nom="Dupont",
        prenom="Marie",
        email="marie.dupont@example.com",
        mot_de_passe="Secret123"
    )
    expected_user = {
        "id": 5,
        "nom": "Dupont",
        "prenom": "Marie",
        "email": "marie.dupont@example.com",
        "status_actif": True
    }
    called_with_id = {}
    def fake_get_user(user_id: int):
        called_with_id["id"] = user_id
        return expected_user
    service.get_utilisateur_by_id = fake_get_user
    result = service.edit_user(5, data)

    assert cursor.last_query == (
        "UPDATE utilisateur SET nom=%s, prenom=%s, email=%s, mot_de_passe=%s WHERE utilisateur_id=%s"
    )
    assert cursor.last_values == [
        "Dupont",
        "Marie",
        "marie.dupont@example.com",
        "Secret123",
        5,
    ]
    assert called_with_id["id"] == 5
    assert result == expected_user

def test_edit_user_utilisateur_non_trouve():
    cursor = FakeCursor()
    fake_db = FakeDB(cursor)
    service = UserServices(fake_db)

    data = UtilisateurModify(
        nom="Test",
        prenom="User",
        email="test.user@example.com",
        mot_de_passe="Password123"
    )
    called_with_id = {}
    def fake_get_user(user_id: int):
        called_with_id["id"] = user_id
        return None 

    service.get_utilisateur_by_id = fake_get_user
    result = service.edit_user(42, data)

    assert cursor.last_query == (
        "UPDATE utilisateur SET nom=%s, prenom=%s, email=%s, mot_de_passe=%s WHERE utilisateur_id=%s"
    )
    assert cursor.last_values == [
        "Test",
        "User",
        "test.user@example.com",
        "Password123",
        42,
    ]
    assert called_with_id["id"] == 42
    assert result is None


#test suppresion de compte
def test_delete_user_succes():
    cursor = FakeCursor(rowcount=1)  
    fake_db = FakeDB(cursor)
    service = UserServices(fake_db)
    result = service.delete_user(10)

    assert cursor.last_query == "DELETE FROM utilisateur WHERE utilisateur_id = %s"
    assert cursor.last_values == (10,)
    assert fake_db.commit_called is True
    assert result is True

def test_delete_user_echec():
    cursor = FakeCursor(rowcount=0)
    fake_db = FakeDB(cursor)
    service = UserServices(fake_db)
    result = service.delete_user(999)

    assert cursor.last_query == "DELETE FROM utilisateur WHERE utilisateur_id = %s"
    assert cursor.last_values == (999,)
    assert fake_db.commit_called is True
    assert result is False










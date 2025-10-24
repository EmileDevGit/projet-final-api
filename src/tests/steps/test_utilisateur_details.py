import requests
from pytest_bdd import scenarios, given, then, when, parsers

scenarios("../features/utilisateurs/details.feature")

BASE_URL = "https://610c7456-d04c-4b0f-b6ec-f5ed88a72eb3.mock.pstmn.io"

@given(parsers.parse("un utilisateur existant ayant l'id {id:d} et le rôle {admin_role}"))
def existing_admin(id, admin_role):
    user = {
        "id": id,
        "nom": "test",
        "prenom": "test",
        "role": admin_role
    }
    response = requests.post(f"{BASE_URL}/utilisateurs", json=user)
    assert response.status_code == 201
    return user

@given(parsers.parse("un utilisateur existant ayant l'id {user_id:d}"))
def existing_user(user_id):
    user = {
        "id": user_id,
        "nom": "test",
        "prenom": "test",
        "role": "user"
    }
    response = requests.post(f"{BASE_URL}/utilisateurs", json=user)
    assert response.status_code == 201
    return user



@given(parsers.parse("un utilisateur authentifie ayant le role {user_role}, l'id {user_id:d} et le prenom {prenom}"))
def existing_user_with_name(user_id, user_role, prenom):
    user = {
        "id": user_id,
        "nom": "test",
        "prenom": prenom,
        "role": user_role 
    }
    response = requests.post(f"{BASE_URL}/utilisateurs", json=user)
    assert response.status_code == 201
    return user

@given(parsers.parse("un utilisateur inexistant ayant l'id {user_id:d}"))
def non_existing_user(user_id):
    response = requests.delete(f"{BASE_URL}/utilisateurs/{user_id}")
    assert response.status_code == 200

@when(parsers.parse("je fais un fetch sur l'utilisateur ayant l'id {user_id:d}"))
def fetch_user(user_id, request):
    response = requests.get(f"{BASE_URL}/utilisateurs/{user_id}")
    request._user_api_response = response
    return response

@then(parsers.parse("le statut de reponse devrait etre {code:d}"))
def validation_code_retour(code, request):
    assert request._user_api_response.status_code == code 

@then(parsers.parse("le corps de reponse contient un utilisateur ayant l'id {user_id:d}"))
def validate_user_id(user_id, request):
    data = request._user_api_response.json()
    user_data = data.get("data", {})
    assert user_data.get("utilisateur_id") == user_id

@then(parsers.parse("le corps de reponse contient le message \"{message}\""))
def validate_errror_message(message, request):
    data = request._user_api_response.json()
    assert data.get("error") == message


@then(parsers.parse("le l'utilisateur retourne possede le role {user_role} et le prenom {prenom}"))
def validate_user_role_prenom(user_role, prenom, request):
    data = request._user_api_response.json()
    user_data = data.get("data", {})
    assert user_data.get("prenom") == prenom
    assert user_data.get("role") == user_role



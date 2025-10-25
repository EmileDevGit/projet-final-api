import requests
from pytest_bdd import scenarios, given, then, when, parsers

scenarios("../features/utilisateurs/liste.feature")

BASE_URL = "https://610c7456-d04c-4b0f-b6ec-f5ed88a72eb3.mock.pstmn.io"

@given("un administrateur existant")
def existing_admin():
    admin = {
        "id": 1,
        "nom": "Admin",
        "prenom": "System",
        "role": "admin"
    }
    response = requests.post(f"{BASE_URL}/utilisateurs", json=admin)
    assert response.status_code in [200, 201], "Impossible de créer ou retrouver l'administrateur"
    return admin


@given(parsers.parse("un utilisateur existant avec le rôle {user_role}"))
def existing_user(user_role):
    user = {
        "id": 2,
        "nom": "User",
        "prenom": "Lambda",
        "role": user_role
    }
    response = requests.post(f"{BASE_URL}/utilisateurs", json=user)
    assert response.status_code in [200, 201], f"Échec création utilisateur rôle {user_role}"
    return user

@when(parsers.parse("il fais un fetch sur touts les utilisateurs"))
def fetch_all_users(request):
    response = requests.get(f"{BASE_URL}/utilisateurs")
    request._user_api_response = response
    return response


@when(parsers.parse("il fais un fetch sur les utilisateurs avec le mot-cle {mot_cle} en parametre"))
def fetch_users_with_filter(request, mot_cle):
    response = requests.get(f"{BASE_URL}/utilisateurs", params={"mot-cle": mot_cle})
    request._user_api_response = response
    return response


@when("il fais un fetch sur les utilisateurs")
def fetch_users(request):
    response = requests.get(f"{BASE_URL}/utilisateurs")
    request._user_api_response = response
    return response

@then(parsers.parse("il recoit un code {code:d}"))
def check_status_code(code, request):
    assert request._user_api_response.status_code == code, (
        f"Code reçu: {request._user_api_response.status_code}, attendu: {code}"
    )


@then(parsers.parse("il recoit un tableau json nommé {json_name}"))
def check_json_array_name(json_name, request):
    data = request._user_api_response.json()
    assert json_name in data, f"Le champ '{json_name}' est manquant dans la réponse"
    assert isinstance(data[json_name], list), f"'{json_name}' devrait être un tableau JSON"


@then(parsers.parse("les utilisateurs dans le tableau ont la chaîne {mot_cle} dans leur contenu"))
def check_users_contain_keyword(mot_cle, request):
    data = request._user_api_response.json()
    utilisateurs = data.get("utilisateurs", [])
    assert utilisateurs, "La liste 'utilisateurs' est vide"
    assert all(
        mot_cle.lower() in str(u).lower() for u in utilisateurs
    ), f"Aucun utilisateur ne contient la chaîne '{mot_cle}'"


@then("les utilisateurs dans le tableau ont le rôle mentor")
def check_users_role_mentor(request):
    data = request._user_api_response.json()
    utilisateurs = data.get("utilisateurs", [])
    assert utilisateurs, "La liste 'utilisateurs' est vide"
    assert all(
        u.get("role") == "mentor" for u in utilisateurs
    ), "Tous les utilisateurs devraient avoir le rôle 'mentor'"


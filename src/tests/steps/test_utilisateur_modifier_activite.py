import requests
from pytest_bdd import scenarios, given, then, when, parsers

scenarios("../features/utilisateurs/details.feature")

BASE_URL = "https://610c7456-d04c-4b0f-b6ec-f5ed88a72eb3.mock.pstmn.io"

@given(parsers.parse("un utilisateur authentifie ayant le role {user_role}"))
@given(parsers.parse("un utilisateur authentifie ayant le role {user_role}, l'id {user_id:d}"))
@given(parsers.parse("un utilisateur authentifie ayant le role {user_role}, l'id {user_id:d} et le statut {status}"))
def authenticated_user(user_role, user_id=None, status=None):
    user = {
        "role": user_role,
        "id": user_id or 1,
        "nom": "Test",
        "prenom": "Auth",
    }
    if status:
        user["statut"] = status

    response = requests.post(f"{BASE_URL}/utilisateurs", json=user)
    assert response.status_code in [200, 201], f"Erreur création utilisateur {user}"
    return user


@given(parsers.parse("un utilisateur existant ayant l'id {user_id:d} et un statut {status}"))
def existing_user_with_status(user_id, status):
    user = {
        "id": user_id,
        "nom": "Test",
        "prenom": "User",
        "role": "user",
        "statut": status
    }
    response = requests.post(f"{BASE_URL}/utilisateurs", json=user)
    assert response.status_code in [200, 201], f"Erreur création utilisateur existant id={user_id}"
    return user


@given(parsers.parse("un utilisateur inexistant ayant l'id {user_id:d}"))
def non_existing_user(user_id):
    response = requests.delete(f"{BASE_URL}/utilisateurs/{user_id}")
    assert response.status_code in [200, 404]
    return {"id": user_id}

@when(parsers.parse("il fais un put sur l'utilisateur ayant l'id {user_id:d} changeant son statut pour {status}"))
def admin_put_user_status(request, user_id, status):
    response = requests.put(f"{BASE_URL}/utilisateurs/{user_id}", json={"statut": status})
    request._user_api_response = response
    return response


@when(parsers.parse("il fais un patch sur l'utilisateur ayant l'id {user_id:d} changeant son statut pour {status}"))
@when(parsers.parse("il fais un patch sur l'utilisateur ayant l'id {user_id:d} changeant le statut pour {status}"))
def patch_user_status(request, user_id, status):
    response = requests.patch(f"{BASE_URL}/utilisateurs/{user_id}", json={"statut": status})
    request._user_api_response = response
    return response


@when(parsers.parse("il fais un patch sur l'utilisateur ayant l'id {user_id:d}"))
def patch_user_without_body(request, user_id):
    response = requests.patch(f"{BASE_URL}/utilisateurs/{user_id}")
    request._user_api_response = response
    return response

@then(parsers.parse("le statut de reponse devrait etre {code:d}"))
def check_status_code(request, code):
    assert request._user_api_response.status_code == code, (
        f"Code HTTP {request._user_api_response.status_code}, attendu {code}"
    )

@then(parsers.parse('le corps de reponse contient un utilisateur ayant l\'id {user_id:d} et un statut {status}'))
def check_user_status_in_body(request, user_id, status):
    data = request._user_api_response.json()
    assert "utilisateur" in data, "Le champ 'utilisateur' est manquant dans la réponse"
    utilisateur = data["utilisateur"]
    assert utilisateur.get("id") == user_id, f"id attendu {user_id}, obtenu {utilisateur.get('id')}"
    assert utilisateur.get("statut") == status, f"statut attendu '{status}', obtenu '{utilisateur.get('statut')}'"

@then(parsers.parse('le corps de reponse contient le message "{message}"'))
def check_message_in_response(request, message):
    data = request._user_api_response.json()
    assert "message" in data, "Aucun message trouvé dans la réponse"
    assert data["message"].lower() == message.lower(), (
        f"Message attendu '{message}', obtenu '{data['message']}'"
    )

from app.services.service_utilisateurs import UserServices
from data.models.model_utilisateur import UtilisateurModify
from data.dao.I_dao_utilisateur import IUtilisateurDAO as IUtilisateurDAO
from unittest.mock import create_autospec


# test obtenir list des utilisateur
def test_get_all_utilisateurs():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.get_all_utilisateurs.return_value = [
        {
            "utilisateur_id": 1,
            "nom": "Dupont",
            "prenom": "Marie",
            "email": "marie@example.com",
            "type_compte": "ADMIN",
            "status_actif": True,
        },
        {
            "utilisateur_id": 2,
            "nom": "Martin",
            "prenom": "Jean",
            "email": "jean@example.com",
            "type_compte": "MENTOR",
            "status_actif": False,
        }
    ]

    service = UserServices(mockDAO)
    result = service.get_all_utilisateurs()
    assert len(result) == 2
    mockDAO.get_all_utilisateurs.assert_called_once()


# test obtenir list mentor


def test_get_all_mentors():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.get_all_mentors.return_value = [
        {
            "utilisateur_id": 1,
            "nom": "Dupont",
            "prenom": "Charles",
            "email": "charles@example.com",
            "type_compte": "MENTOR",
            "status_actif": True,
        },
        {
            "utilisateur_id": 2,
            "nom": "Martin",
            "prenom": "Jean",
            "email": "jean@example.com",
            "type_compte": "MENTOR",
            "status_actif": False,
        },
    ]

    service = UserServices(mockDAO)
    result = service.get_all_mentors()
    assert len(result) == 2
    mockDAO.get_all_mentors.assert_called_once()


# test recherche utilisateur par id
def test_get_utilisateur_by_id_succes():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.get_utilisateur_by_id.return_value = {
        "utilisateur_id": 5,
        "nom": "Dupont",
        "prenom": "Marie",
        "email": "marie.dupont@example.com",
        "type_compte": "ADMIN",
        "status_actif": True,
    }
    service = UserServices(mockDAO)
    result = service.get_utilisateur_by_id(5)
    assert result.id == 5
    assert result.nom == "Dupont"
    assert result.prenom == "Marie"
    assert result.email == "marie.dupont@example.com"
    assert result.type_compte == "ADMIN"
    assert result.status_actif
    mockDAO.get_utilisateur_by_id.assert_called_once_with(5)


def test_get_utilisateur_by_id_utilisateur_non_trouve():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.get_utilisateur_by_id.return_value = {}
    service = UserServices(mockDAO)
    result = service.get_utilisateur_by_id(999)
    assert result is None
    mockDAO.get_utilisateur_by_id.assert_called_once_with(999)


# test changement de status
def test_update_user_status_succes():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.update_user_status.return_value = {
        "utilisateur_id": 2,
        "nom": "Dupont",
        "prenom": "Marie",
        "email": "marie.dupont@example.com",
        "type_compte": "ADMIN",
        "status_actif": False,
    }
    service = UserServices(mockDAO)
    result = service.update_user_status(2, False)
    assert result.id == 2
    assert result.nom == "Dupont"
    assert result.prenom == "Marie"
    assert result.email == "marie.dupont@example.com"
    assert result.type_compte == "ADMIN"
    assert result.status_actif is False
    mockDAO.update_user_status.assert_called_once_with(2, False)


def test_update_user_status_utilisateur_non_trouve():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.update_user_status.return_value = {}
    service = UserServices(mockDAO)
    result = service.update_user_status(2, False)
    assert result is None
    mockDAO.update_user_status.assert_called_once_with(2, False)


# test modification utilisateur
def test_edit_user_succes():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.edit_user.return_value = {
        "utilisateur_id": 5,
        "nom": "newNom",
        "prenom": "newPrenom",
        "email": "newEmail@example.com",
        "type_compte": "USER",
        "status_actif": True
    }
    service = UserServices(mockDAO)

    data = UtilisateurModify(
        nom="newNom",
        prenom="newPrenom",
        email="newEmail@example.com",
        mot_de_passe="Secret123@"
    )

    result = service.edit_user(5, data)
    assert result.nom == "newNom"
    assert result.prenom == "newPrenom"
    assert result.email == "newEmail@example.com"
    mockDAO.edit_user.assert_called_once_with(5, data)


def test_edit_user_utilisateur_non_trouve():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.edit_user.return_value = {}
    service = UserServices(mockDAO)

    data = UtilisateurModify(
        nom="newNom",
        prenom="newPrenom",
        email="newEmail@example.com",
        mot_de_passe="Secret123@"
    )

    result = service.edit_user(999, data)
    assert result is None
    mockDAO.edit_user.assert_called_once_with(999, data)


# test suppresion de compte
def test_delete_user_succes():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.get_utilisateur_by_id.return_value = {
        "utilisateur_id": 1,
        "nom": "Dupont",
        "prenom": "Charles",
        "email": "charles@example.com",
        "type_compte": "MENTOR",
        "status_actif": True,
    }
    mockDAO.delete_user.return_value = True
    service = UserServices(mockDAO)
    result = service.delete_user(1)
    assert result
    mockDAO.get_utilisateur_by_id.assert_called_once_with(1)
    mockDAO.delete_user.assert_called_once_with(1)


def test_delete_user_echec():
    mockDAO = create_autospec(IUtilisateurDAO)
    mockDAO.edit_user.return_value = {}
    mockDAO.delete_user.return_value = False
    service = UserServices(mockDAO)

    result = service.delete_user(999)
    assert result is False
    mockDAO.get_utilisateur_by_id.assert_called_once_with(999)
    mockDAO.delete_user.assert_called_once_with(999)

import pytest
from unittest.mock import create_autospec
from fastapi import HTTPException
from app.services.service_ressource import RessourceService
from app.data.dao.I_dao_ressource import IRessourceDAO
from app.data.models.model_ressource import RessourceResponse, RessourceCreate, RessourceModify


def test_get_all_ressources_sans_filtre():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_all_ressources.return_value = [
        {
            "ressource_id": 1,
            "titre": "Intro Python",
            "description": "Bases de Python",
            "url_ressource": "http://example.com/r1",
            "visibilite": True,
            "categorie_id": 10,
            "auteur_id": 1,
        },
        {
            "ressource_id": 2,
            "titre": "FastAPI avancé",
            "description": "API modernes",
            "url_ressource": "http://example.com/r2",
            "visibilite": False,
            "categorie_id": 11,
            "auteur_id": 2,
        },
    ]
    service = RessourceService(mockDAO)
    result = service.get_all_ressources()
    assert len(result) == 2
    assert isinstance(result[0], RessourceResponse)
    assert result[0].id == 1
    mockDAO.get_all_ressources.assert_called_once()
    mockDAO.get_filtered_ressources.assert_not_called()

def test_get_all_ressources_avec_filtre():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_filtered_ressources.return_value = [
        {
            "ressource_id": 1,
            "titre": "Intro Python",
            "description": "Bases de Python",
            "url_ressource": "http://example.com/r1",
            "visibilite": True,
            "categorie_id": 10,
            "auteur_id": 1,
        }
    ]
    service = RessourceService(mockDAO)
    result = service.get_all_ressources(q="python")
    assert len(result) == 1
    assert result[0].titre == "Intro Python"
    mockDAO.get_filtered_ressources.assert_called_once_with("python")
    mockDAO.get_all_ressources.assert_not_called()

def test_get_all_ressources_aucune_ressource():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_all_ressources.return_value = []
    service = RessourceService(mockDAO)
    result = service.get_all_ressources()
    assert result is None
    mockDAO.get_all_ressources.assert_called_once()


def test_search_ressources_by_name_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_filtered_ressources.return_value = [
        {
            "ressource_id": 1,
            "titre": "Intro Python",
            "description": "Bases",
            "url_ressource": "http://example.com/r1",
            "visibilite": True,
            "categorie_id": 10,
            "auteur_id": 1,
        }
    ]
    service = RessourceService(mockDAO)
    result = service.search_ressources_by_name("Python")
    assert len(result) == 1
    assert result[0].titre == "Intro Python"
    mockDAO.get_filtered_ressources.assert_called_once_with("Python")

def test_search_ressources_by_name_aucun_resultat():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_filtered_ressources.return_value = []
    service = RessourceService(mockDAO)
    result = service.search_ressources_by_name("Inexistant")
    assert result is None
    mockDAO.get_filtered_ressources.assert_called_once_with("Inexistant")


def test_get_ressource_by_id_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressource_by_id.return_value = {
        "ressource_id": 5,
        "titre": "Intro Python",
        "description": "Bases",
        "url_ressource": "http://example.com/r5",
        "visibilite": True,
        "categorie_id": 10,
        "auteur_id": 1,
    }
    service = RessourceService(mockDAO)
    result = service.get_ressource_by_id(5)
    assert isinstance(result, RessourceResponse)
    assert result.id == 5
    assert result.titre == "Intro Python"
    mockDAO.get_ressource_by_id.assert_called_once_with(5)

def test_get_ressource_by_id_non_trouve():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressource_by_id.return_value = {}
    service = RessourceService(mockDAO)
    result = service.get_ressource_by_id(999)
    assert result is None
    mockDAO.get_ressource_by_id.assert_called_once_with(999)


def test_get_ressources_by_categorie_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressources_by_categorie.return_value = [
        {
            "ressource_id": 1,
            "titre": "R1",
            "description": "Desc R1",
            "url_ressource": "http://example.com/r1",
            "visibilite": True,
            "categorie_id": 3,
            "auteur_id": 1,
        },
        {
            "ressource_id": 2,
            "titre": "R2",
            "description": "Desc R2",
            "url_ressource": "http://example.com/r2",
            "visibilite": False,
            "categorie_id": 3,
            "auteur_id": 2,
        },
    ]
    service = RessourceService(mockDAO)
    result = service.get_ressources_by_categorie(3)
    assert len(result) == 2
    assert all(r.categorie_id == 3 for r in result)
    mockDAO.get_ressources_by_categorie.assert_called_once_with(3)

def test_get_ressources_by_categorie_aucun_resultat():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressources_by_categorie.return_value = []
    service = RessourceService(mockDAO)
    result = service.get_ressources_by_categorie(3)
    assert result is None
    mockDAO.get_ressources_by_categorie.assert_called_once_with(3)


def test_get_ressources_by_auteur_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressources_by_auteur.return_value = [
        {
            "ressource_id": 1,
            "titre": "R1",
            "description": "Desc R1",
            "url_ressource": "http://example.com/r1",
            "visibilite": True,
            "categorie_id": 3,
            "auteur_id": 7,
        }
    ]

    service = RessourceService(mockDAO)
    result = service.get_ressources_by_auteur(7)
    assert len(result) == 1
    assert result[0].auteur_id == 7
    mockDAO.get_ressources_by_auteur.assert_called_once_with(7)

def test_get_ressources_by_auteur_aucun_resultat():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressources_by_auteur.return_value = []
    service = RessourceService(mockDAO)
    result = service.get_ressources_by_auteur(7)
    assert result is None
    mockDAO.get_ressources_by_auteur.assert_called_once_with(7)


def test_edit_ressource_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.edit_ressource.return_value = {
        "ressource_id": 5,
        "titre": "Nouveau titre",
        "description": "Nouvelle description",
        "url_ressource": "http://example.com/r5",
        "visibilite": True,
        "categorie_id": 10,
        "auteur_id": 1,
    }
    service = RessourceService(mockDAO)
    data = RessourceModify(
        titre="Nouveau titre",
        description="Nouvelle description",
        url_ressource="http://example.com/r5",
        visibilite=True,
        categorie_id=10,
    )
    result = service.edit_ressource(5, data)
    assert isinstance(result, RessourceResponse)
    assert result.id == 5
    assert result.titre == "Nouveau titre"
    assert result.visibilite is True
    mockDAO.edit_ressource.assert_called_once_with(5, data)

def test_edit_ressource_non_trouve():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.edit_ressource.return_value = {}
    service = RessourceService(mockDAO)
    data = RessourceModify(
        titre="Nouveau titre",
        description="Nouvelle description",
        url_ressource="http://example.com/r999",
        visibilite=True,
        categorie_id=10,
    )
    result = service.edit_ressource(999, data)
    assert result is None
    mockDAO.edit_ressource.assert_called_once_with(999, data)


def test_update_ressource_visibility_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.update_ressource_visibility.return_value = {
        "ressource_id": 3,
        "titre": "R1",
        "description": "Desc R1",
        "url_ressource": "http://example.com/r3",
        "visibilite": False,
        "categorie_id": 4,
        "auteur_id": 2,
    }
    service = RessourceService(mockDAO)
    result = service.update_ressource_visibility(3, False)
    assert isinstance(result, RessourceResponse)
    assert result.id == 3
    assert result.visibilite is False
    mockDAO.update_ressource_visibility.assert_called_once_with(3, False)

def test_update_ressource_visibility_non_trouve():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.update_ressource_visibility.return_value = {}
    service = RessourceService(mockDAO)
    result = service.update_ressource_visibility(3, False)
    assert result is None
    mockDAO.update_ressource_visibility.assert_called_once_with(3, False)


def test_delete_ressource_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressource_by_id.return_value = {
        "ressource_id": 1,
        "titre": "R1",
        "description": "Desc R1",
        "url_ressource": "http://example.com/r1",
        "visibilite": True,
        "categorie_id": 3,
        "auteur_id": 1,
    }
    mockDAO.delete_ressource.return_value = True
    service = RessourceService(mockDAO)
    result = service.delete_ressource(1)
    assert result is True
    mockDAO.get_ressource_by_id.assert_called_once_with(1)
    mockDAO.delete_ressource.assert_called_once_with(1)

def test_delete_ressource_non_trouve():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressource_by_id.return_value = None
    service = RessourceService(mockDAO)
    result = service.delete_ressource(999)
    assert result is None
    mockDAO.get_ressource_by_id.assert_called_once_with(999)
    mockDAO.delete_ressource.assert_not_called()

def test_delete_ressource_echec_suppression():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.get_ressource_by_id.return_value = {
        "ressource_id": 1,
        "titre": "R1",
        "description": "Desc R1",
        "url_ressource": "http://example.com/r1",
        "visibilite": True,
        "categorie_id": 3,
        "auteur_id": 1,
    }
    mockDAO.delete_ressource.return_value = False
    service = RessourceService(mockDAO)
    result = service.delete_ressource(1)
    assert result is False
    mockDAO.get_ressource_by_id.assert_called_once_with(1)
    mockDAO.delete_ressource.assert_called_once_with(1)


def test_create_ressource_succes():
    mockDAO = create_autospec(IRessourceDAO)
    mockDAO.create_ressource.return_value = {
        "ressource_id": 10,
        "titre": "Nouvelle ressource",
        "description": "Description valide",
        "url_ressource": "http://example.com/r10",
        "visibilite": True,
        "categorie_id": 5,
        "auteur_id": 3,
    }
    service = RessourceService(mockDAO)
    data = RessourceCreate(
        titre="Nouvelle ressource",
        description="Description valide",
        url_ressource="http://example.com/r10",
        categorie_id=5,
        auteur_id=3,
        visibilite=True,
    )
    result = service.create_ressource(data)
    assert result["ressource_id"] == 10
    assert result["titre"] == "Nouvelle ressource"
    assert result["visibilite"] is True
    mockDAO.create_ressource.assert_called_once_with(data)
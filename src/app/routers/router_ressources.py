from fastapi import APIRouter, Depends, HTTPException
from data.connexion import mydb as db
from data.dao.dao_ressource import RessourceDAO
from services.service_ressource import RessourceService
from utils.auth import verify_token
from data.models.model_ressource import RessourceModify, RessourceCreate
print(">>> Chargement router_ressources")


ressources_router = APIRouter(prefix="/ressources")

def get_dao():
    return RessourceDAO(db)

def get_service(dao: RessourceDAO = Depends(get_dao)):
    return RessourceService(dao)


@ressources_router.get("/")
async def get_ressources(
    q: str | None = None,
    user: dict = Depends(verify_token),
    service: RessourceService = Depends(get_service)
):
    ressources = service.get_all_ressources(q) or []

    role = user["role"]
    user_id = user["id"]

    if role == "ADMIN":
        return ressources

    return [r for r in ressources if r.visibilite or r.auteur_id == user_id]

@ressources_router.get("/{id}")
async def get_ressource_by_id(
    id: int,
    user: dict = Depends(verify_token),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user["role"]
    user_id = user["id"]

    if role == "ADMIN":
        return res

    if res.visibilite or res.auteur_id == user_id:
        return res

    raise HTTPException(403, "Accès refusé : vous ne pouvez consulter que vos propre ressouces")


@ressources_router.post("/")
async def create_ressource(
    data: RessourceCreate,
    user: dict = Depends(verify_token),
    service: RessourceService = Depends(get_service)
):
    role = user["role"]

    if role == "ADMIN":
        return service.create_ressource(data)

    if role == "MENTOR":
        data.auteur_id = user["id"]
        return service.create_ressource(data)

    if role == "USER":
        data.visibilite = False  
        data.auteur_id = user["id"]
        return service.create_ressource(data)

    raise HTTPException(403, "Accès interdit")


@ressources_router.put("/{id}")
async def update_ressource(
    id: int,
    data: RessourceModify,
    user: dict = Depends(verify_token),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user["role"]
    user_id = user["id"]

    if role == "ADMIN":
        return service.edit_ressource(id, data)

    if res.auteur_id == user_id:
        return service.edit_ressource(id, data)

    raise HTTPException(403, "Vous ne pouvez modifier que vos propres ressources")


@ressources_router.patch("/{id}")
async def update_visibility(
    id: int,
    visible: bool,
    user: dict = Depends(verify_token),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user["role"]
    user_id = user["id"]

    if role == "ADMIN":
        return service.update_ressource_visibility(id, visible)


    if res.auteur_id == user_id:
        return service.update_ressource_visibility(id, visible)

    raise HTTPException(403, "Vous ne pouvez modifier que vos propres ressources")


@ressources_router.delete("/{id}")
async def delete_ressource(
    id: int,
    user: dict = Depends(verify_token),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user["role"]
    user_id = user["id"]

    if role == "ADMIN":
        service.delete_ressource(id)
        return {"message": "Ressource supprimée avec succès"}

    if res.auteur_id == user_id:
        service.delete_ressource(id)
        return {"message": "Ressource supprimée avec succès"}

    raise HTTPException(403, "Vous ne pouvez supprimer que vos propres ressources")

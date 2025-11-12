from fastapi import APIRouter, Depends, HTTPException
from data.connexion import mydb as db
from services.service_utilisateurs import UserServices as UserServices
from utils.auth import *


users_router = APIRouter(prefix="/utilisateurs")

service = UserServices(db)


@users_router.get("/")
async def get_users(user=Depends(verify_token), filter: str | None = None):
    if user["role"] in ["ADMIN"]:
        return service.get_all_utilisateurs(filter)
    else:
        return service.get_all_mentors()


@users_router.get("/token")
async def get_auth_token(id:int, role: str):
    data = {"id": id, "email": "test@token.gmail", "role": role}
    token = create_access_token(data)
    return {"access_token": token}


@users_router.get("/{id}")
async def get_user_by_id(id: int, user=Depends(verify_token)):
    if user["role"] == "ADMIN":
        utilisateur = service.get_utilisateur_by_id(id)
        #404 si utilisateur existe pas
        if not utilisateur:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return utilisateur

    elif user["id"] == id:
        utilisateur = service.get_utilisateur_by_id(id)
        if not utilisateur:
            #404 si utilisateur existe pas
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return utilisateur

    else:
        #403 si l'utilisateur n'a pas les droit admin
        raise HTTPException(status_code=403,detail="Accès refusé : vous ne pouvez consulter que votre propre profil")

@ users_router.post("/")
async def post_users():
    return {"message": "Création d'un utilisateur"}


@ users_router.put("/{id}")
async def put_user(id: int):
    return {"message": "Modification d'un utilisateur"}


@ users_router.patch("/{id}")
async def patch_user_visibility(id: int, actif: bool):
    return {"message": f"L'utilisateur avec l'id {id} est mis à jour actif: {actif}"}


@ users_router.delete("/{id}")
async def delete_user(id: int):
    return {"message": f"L'utilisateur avec l'id {id} à été supprimé"}

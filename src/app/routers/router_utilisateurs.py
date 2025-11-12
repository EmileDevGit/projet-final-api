from fastapi import APIRouter, Depends, HTTPException
from data.connexion import mydb as db
from services.service_utilisateurs import UserServices as UserServices
from utils.auth import *


users_router = APIRouter(prefix="/utilisateurs")

service = UserServices(db)


@users_router.get("/")
async def get_users(user=Depends(verify_token)):
    if user["role"] in ["ADMIN"]:
        return service.get_all_utilisateurs()
    else:
        return service.get_all_mentors()


@users_router.get("/token")
async def get_auth_token(role: str):
    data = {"sub": "test@token.gmail", "role": role}
    token = create_access_token(data)
    return {"access_token": token}


@ users_router.get("/{id}")
async def get_user_by_id(id: int):
    return {"message": "Un utilisateurs particulier"}


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

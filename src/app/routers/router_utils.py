from fastapi import APIRouter, Depends, HTTPException
from data.connexion import mydb as db
from services.service_utils import UtilsServices as UtilsServices
from utils.auth import *
from data.models.model_utilisateur import UtilisateurLogin as UtilisateurLogin

utils_router = APIRouter(prefix="/auth")

service = UtilsServices(db)


@utils_router.post("/register")
async def post_register():
    return service.register()


@utils_router.post("/login")
async def post_login(creds: UtilisateurLogin):
    return service.login(creds)

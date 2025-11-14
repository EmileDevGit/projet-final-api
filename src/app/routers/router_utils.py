from fastapi import APIRouter
from data.connexion import mydb as db
from services.service_utils import UtilsServices as UtilsServices
from data.models.model_utilisateur import UtilisateurLogin as UtilisateurLogin
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate


utils_router = APIRouter(prefix="/auth")

service = UtilsServices(db)


@utils_router.post("/register")
async def post_register(user_data: UtilisateurCreate):
    return service.register(user_data)


@utils_router.post("/login")
async def post_login(creds: UtilisateurLogin):
    return service.login(creds)

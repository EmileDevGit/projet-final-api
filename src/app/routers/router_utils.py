from fastapi import APIRouter, Depends
from data.connexion import mydb as db
from services.service_utils import UtilsServices as UtilsServices
from data.models.model_utilisateur import UtilisateurLogin as UtilisateurLogin
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from data.dao.dao_utilisateur import UtilisateurDAO as UtilisateurDAO


utils_router = APIRouter(prefix="/auth")

# Gestion des dépendances
def get_dao():
    return UtilisateurDAO(db)


def get_service(dao: UtilisateurDAO = Depends(get_dao)):
    return UtilsServices(dao)


# Routes utilitaires
@utils_router.post("/register")
async def post_register(
        user_data: UtilisateurCreate,
        service: UtilsServices = Depends(get_service)):
    return service.register(user_data)


@utils_router.post("/login")
async def post_login(
        creds: UtilisateurLogin,
        service: UtilsServices = Depends(get_service)):
    return service.login(creds)

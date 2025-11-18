from fastapi import APIRouter, Depends
from app.data.connexion import mydb as db
from app.services.service_utils import UtilsServices as UtilsServices
from app.data.models.model_utilisateur import UtilisateurLogin as UtilisateurLogin
from app.data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from app.data.dao.dao_utilisateur import UtilisateurDAO as UtilisateurDAO


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

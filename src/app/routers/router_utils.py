from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.data.connexion import mydb as db
from app.services.service_utils import UtilsServices
from app.services.service_auth import AuthServices
from app.data.models.model_utilisateur import UtilisateurCreate
from app.data.dao.dao_utilisateur import UtilisateurDAO


utils_router = APIRouter(prefix="/auth")


def get_dao():
    return UtilisateurDAO(db)


def get_service(dao: UtilisateurDAO = Depends(get_dao)):
    return UtilsServices(dao)


def get_auth_service(dao: UtilisateurDAO = Depends(get_dao)):
    return AuthServices(dao)


@utils_router.post("/register")
async def post_register(
        user_data: UtilisateurCreate,
        service: UtilsServices = Depends(get_service)
):
    return service.register(user_data)


@utils_router.post("/login")
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthServices = Depends(get_auth_service)
):
    print(f"Trying to login: email={form_data.username}, password={form_data.password}")
    return service.authenticate_and_issue_token(
        email=form_data.username,
        password=form_data.password
    )

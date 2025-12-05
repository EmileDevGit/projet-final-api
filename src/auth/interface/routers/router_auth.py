from fastapi import APIRouter, Depends, Form
from starlette import status

from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded
from auth.services.services_auth import TokenServices
from auth.data.dao.dao_auth import AuthDAO
from app.data.connexion import mydb as db

router = APIRouter()


def get_dao():
    return AuthDAO(db)


def get_service(dao: AuthDAO = Depends(get_dao)):
    return TokenServices(dao)


@router.post("/token")
def authenticate(
    sub: str = Form(...),
    id: int = Form(...),
    role: str = Form(...),
    service: TokenServices = Depends(get_service)
):
    user_data = {
        "sub": sub,
        "id": id,
        "role": role
    }
    return service.issue_token(user_data)


@router.post("/token/validate")
def validate(
    token: str = Form(...),
    service: TokenServices = Depends(get_service)
) -> TokenViewDecoded:
    print(f"Received Token: {token}")
    return service.validate_token(token)

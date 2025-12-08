from fastapi import APIRouter, Depends, Form, HTTPException
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
    try:
        user_data = {
            "sub": sub,
            "id": id,
            "role": role
        }
        return service.issue_token(user_data)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur du serveur lors de l'attribution du token d'access"
        )


@router.post("/token/refresh")
def refresh(
    refresh_token: str = Form(...),
    old_access_token: str = Form(...),
    service: TokenServices = Depends(get_service)
):
    try:
        if not refresh_token or not old_access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un token d'acces et un refresh token sont necessaires"
            )
        return service.refresh_access_token(refresh_token, old_access_token)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur du serveur lors du rafraichissement du token d'access"
        )


@router.post("/token/validate")
def validate(
    token: str = Form(...),
    service: TokenServices = Depends(get_service)
) -> TokenViewDecoded:
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un token a valider est necessaire"
            )
        print(f"Received Token: {token}")
        return service.validate_token(token)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur du serveur lors de la validation du token d'access"
        )

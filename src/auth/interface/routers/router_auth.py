from fastapi import APIRouter, Depends, Form
from starlette import status

from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded
from auth.services.services_auth import issue_token, validate_token

router = APIRouter()


@router.post("/token")
def authenticate(
    sub: str = Form(...),
    id: int = Form(...),
    role: str = Form(...)
):
    user_data = {
        "sub": sub,
        "id": id,
        "role": role
    }
    return issue_token(user_data)


@router.post("/token/validate")
def validate(token: str = Form(...)) -> TokenViewDecoded:
    print(f"Received Token: {token}")
    return validate_token(token)

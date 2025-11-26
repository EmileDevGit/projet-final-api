import bcrypt
import requests
from fastapi import HTTPException
from starlette import status

from app.config.env import settings
from app.interface.model_view.model_view_token import TokenView
from app.interface.model_view.model_view_token_decoded import TokenViewDecoded
from app.data.models.model_utilisateur import Utilisateur


class AuthServices:
    def __init__(self, dao):
        self.token_endpoint = settings.TOKEN_ENDPOINT
        self.token_validate_endpoint = settings.TOKEN_VALIDATE_ENDPOINT
        self.dao = dao

    def authenticate_and_issue_token(
        self,
        email: str,
        password: str
    ) -> TokenView:
        user_data = self.dao.get_utilisateur_by_email(email)
        user = Utilisateur(**user_data)
        print(f"Current user: {user}")

        if not user or not self.verify_password(password, user.mot_de_passe):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print(f"user: {user}")
        try:
            response = requests.post(
                self.token_endpoint,
                data={
                    "sub": user.email,
                    "id": user.id,
                    "role": user.type_compte.value
                }
            )
            print(f"response: {response}")
        except Exception as e:
            print(f"Exception: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to obtain token from auth service",
            )

        token_data = response.json()
        return TokenView(**token_data)

    def validate_token(self, token: str) -> TokenViewDecoded:

        print(f"Sent token: {token}")
        try:
            response = requests.post(
                self.token_validate_endpoint,
                data={"token": token}
            )
            print(f"response: {token}")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if response.status_code == status.HTTP_403_FORBIDDEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=response.json().get("detail")
            )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to validate token from auth service",
            )

        token_data = response.json()
        return TokenViewDecoded(**token_data)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException
from jose import jwt
from starlette import status

from auth.interface.model_view.model_view_token import TokenView
from auth.config.env import settings
from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded
from auth.interface.model_view.model_view_refresh_token_decoded import RefreshTokenViewDecoded


class TokenServices:

    def __init__(self, dao):
        self.dao = dao

    def issue_token(self, user_data: dict) -> TokenView:
        token = self.create_access_token(user_data)
        refresh_token = self.create_refresh_token(user_data)
        return TokenView(access_token=token, refresh_token=refresh_token)

    def create_access_token(self, user_data: dict) -> str:
        to_encode = user_data.copy()
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    def create_refresh_token(self, user_data: dict) -> str:
        jwt_id = uuid.uuid4()
        expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {
            "jwt_id": str(jwt_id),
            "sub": user_data["sub"],
            "exp": int(expire.timestamp())
        }
        refresh_token = jwt.encode(
            to_encode,
            settings.REFRESH_JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        token_data = {
            "jwt_id": str(jwt_id),
            "sub": user_data["sub"],
            "exp": int(expire.timestamp())
        }

        self.dao.save_refresh_token(token_data)
        return refresh_token

    def refresh_access_token(self, refresh_token, old_access_token) -> TokenView:
        try:
            decode_refresh_result = jwt.decode(
                refresh_token,
                settings.REFRESH_JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            refresh_token_decoded = RefreshTokenViewDecoded(**decode_refresh_result)

            decode_access_result = jwt.decode(
                old_access_token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            old_access_token_decoded = TokenViewDecoded(**decode_access_result)
        except Exception as e:
            print(f"Decoding error {e}")
        self.dao.update_refresh_token_state(refresh_token_decoded.jwt_id, True)
        user_data = {
            "sub": old_access_token_decoded.sub,
            "id": old_access_token_decoded.id,
            "role": old_access_token_decoded.role
        }
        new_refresh_token = self.create_refresh_token(user_data)
        new_access_token = self.create_access_token(user_data)

        return TokenView(access_token=new_access_token, refresh_token=new_refresh_token)

    def validate_token(self, token: str) -> TokenViewDecoded:
        decode_result = jwt.decode(token, settings.JWT_SECRET, algorithms=[
            settings.JWT_ALGORITHM])
        token_decoded = TokenViewDecoded(**decode_result)

        if token_decoded.exp < int(datetime.now().timestamp()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Expired token")

        return token_decoded

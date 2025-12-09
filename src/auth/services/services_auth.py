from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, status
from jose import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError


from auth.interface.model_view.model_view_token import TokenView
from auth.config.env import settings
from auth.interface.model_view.model_view_token_decoded import TokenViewDecoded
from auth.interface.model_view.model_view_refresh_token_decoded import RefreshTokenViewDecoded
from auth.data.dao.dao_auth import TokenDatabaseError


class TokenServices:
    def __init__(self, dao):
        self.dao = dao

    def issue_token(self, user_data: dict) -> TokenView:
        token = self.create_access_token(user_data)
        refresh_token = self.create_refresh_token(user_data)
        return TokenView(access_token=token, refresh_token=refresh_token)

    def create_access_token(self, user_data: dict) -> str:
        try:
            to_encode = user_data.copy()
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": int(expire.timestamp())})
            return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        except Exception as e:
            print(f"ERROR: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la creation du token d'access"
            )

    def create_refresh_token(self, user_data: dict) -> str:
        try:
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
        except TokenDatabaseError as e:
            print(f"DATABASE ERROR: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la sauvegarde du token de rafraichissement"
            )
        except Exception as e:
            print(f"ERROR: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la creation du token de rafraichissement"
            )

    def refresh_access_token(self, refresh_token, old_access_token) -> TokenView:
        try:
            decode_refresh_result = jwt.decode(
                refresh_token,
                settings.REFRESH_JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            refresh_token_decoded = RefreshTokenViewDecoded(**decode_refresh_result)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de rafraichissement expire"
            )
        except (InvalidTokenError, DecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de rafraichissement invalide"
            )

        try:
            decode_access_result = jwt.decode(
                old_access_token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": False}
            )
            old_access_token_decoded = TokenViewDecoded(**decode_access_result)
        except (InvalidTokenError, DecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token d'access invalide"
            )

        try:
            self.dao.update_refresh_token_state(refresh_token_decoded.jwt_id, True)
        except TokenDatabaseError as e:
            print(f"DATABASE ERROR: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de l'invalidation du token de rafraichissement"
            )

        user_data = {
            "sub": old_access_token_decoded.sub,
            "id": old_access_token_decoded.id,
            "role": old_access_token_decoded.role
        }
        new_refresh_token = self.create_refresh_token(user_data)
        new_access_token = self.create_access_token(user_data)
        return TokenView(access_token=new_access_token, refresh_token=new_refresh_token)

    def validate_token(self, token: str) -> TokenViewDecoded:
        try:
            decode_result = jwt.decode(
                token, 
                settings.JWT_SECRET, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            token_decoded = TokenViewDecoded(**decode_result)
            return token_decoded
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expire"
            )
        except (InvalidTokenError, DecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Le token fournit est invalide"
            )

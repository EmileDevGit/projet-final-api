from pydantic import BaseModel


class RefreshTokenView(BaseModel):
    refresh_token: str
    token_type: str = "refresh"

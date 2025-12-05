from datetime import datetime
from pydantic import BaseModel


class RefreshTokenViewDecoded(BaseModel):
    jid: str
    user_sub: str
    iat: int
    exp: int

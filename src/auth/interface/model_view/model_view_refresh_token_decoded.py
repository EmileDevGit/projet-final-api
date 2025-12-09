from datetime import datetime
from pydantic import BaseModel


class RefreshTokenViewDecoded(BaseModel):
    jwt_id: str
    sub: str
    exp: int

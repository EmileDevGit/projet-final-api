from datetime import datetime
from pydantic import BaseModel


class TokenViewDecoded(BaseModel):
    id: int
    sub: str
    role: str
    exp: datetime

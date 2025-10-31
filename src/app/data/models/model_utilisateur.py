from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    ADMIN: "ADMIN"
    MENTOR: "MENTOR"
    USER: "USER"


class Utilisateur(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    role: Role
    active: bool


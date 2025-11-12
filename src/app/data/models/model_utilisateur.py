from pydantic import BaseModel, Field
from enum import Enum


class Role(Enum):
    ADMIN: "ADMIN"
    MENTOR: "MENTOR"
    USER: "USER"


class Utilisateur(BaseModel):
    id: int = Field(alias="utilisateur_id")
    nom: str
    prénom: str
    email: str
    type_compte: str
    mot_de_passe: str
    status_actif: bool

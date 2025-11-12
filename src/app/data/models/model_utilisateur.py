from pydantic import BaseModel, Field, field_validator, EmailStr
from enum import Enum


class TypeCompte(str, Enum):
    USER = "user"
    MENTOR = "mentor"
    ADMIN = "admin"

# Modèle utilisateur complet


class Utilisateur(BaseModel):
    id: int = Field(alias="utilisateur_id")
    nom: str
    prénom: str
    email: str
    type_compte: TypeCompte
    mot_de_passe: str
    status_actif: bool


class UtilisateurModify(BaseModel):
    nom: str = Field(..., min_length=2, max_length=50)
    prenom: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    mot_de_passe: str = Field(...)


class UtilisateurLogin(BaseModel):
    email: EmailStr = Field(...)
    mot_de_passe: str = Field(...)


class UtilisateurCreate(BaseModel):
    nom: str = Field(..., min_length=2, max_length=50)
    prenom: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    type_compte: TypeCompte = Field(default=TypeCompte.USER)
    mot_de_passe: str = Field(..., min_length=8)

    @field_validator('mot_de_passe')
    def validate_password(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError(
                'Le mot de passe doit contenir au moins une minuscule')
        if not any(c.isupper() for c in v):
            raise ValueError(
                'Le mot de passe doit contenir au moins une majuscule')
        if not any(c.isdigit() for c in v):
            raise ValueError(
                'Le mot de passe doit contenir au moins un chiffre')
        if len(v) < 8:
            raise ValueError(
                'Le mot de passe doit contenir au moins 8 caractères')
        return v


class UtilisateurResponse(BaseModel):
    id: int = Field(alias="utilisateur_id")
    nom: str
    prenom: str
    email: EmailStr
    type_compte: str
    status_actif: bool

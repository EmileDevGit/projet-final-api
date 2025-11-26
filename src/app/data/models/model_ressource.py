from pydantic import BaseModel, Field, field_validator


class Ressource(BaseModel):
    id: int = Field(alias="ressource_id")
    titre: str
    description: str
    url_ressource: str
    visibilite: bool
    categorie_id: int
    auteur_id: int


class RessourceCreate(BaseModel):
    titre: str = Field(..., min_length=2, max_length=150)
    description: str = Field(..., min_length=5)
    url_ressource: str
    visibilite: bool = Field(default=True)
    categorie_id: int
    auteur_id: int


class RessourceModify(BaseModel):
    titre: str = Field(..., min_length=2, max_length=150)
    description: str = Field(..., min_length=5)
    url_ressource: str
    visibilite: bool
    categorie_id: int


class RessourceResponse(BaseModel):
    id: int = Field(alias="ressource_id")
    titre: str
    description: str
    url_ressource: str
    visibilite: bool
    categorie_id: int
    auteur_id: int

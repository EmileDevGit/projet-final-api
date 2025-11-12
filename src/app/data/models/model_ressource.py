from pydantic import BaseModel

class Ressource(BaseModel):
    id: int 
    titre: str
    description: str
    visibilite: bool
    categorie_id: int
    auteur_id: int


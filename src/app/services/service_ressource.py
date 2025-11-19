from fastapi import HTTPException
from data.models.model_ressource import (
    RessourceResponse,
    RessourceModify,
    RessourceCreate
)


class RessourceService:

    def __init__(self, dao):
        self.dao = dao


    def get_all_ressources(self, q: str | None = None):
        try:
            if q:
                result = self.dao.get_filtered_ressources(q)
            else:
                result = self.dao.get_all_ressources()

            if not result:
                return None

            ressources = [RessourceResponse(**row) for row in result]
            return ressources

        except Exception as e:
            print(f"Erreur lors de la récupération des ressources : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def search_ressources_by_name(self, q: str):
        try:
            result = self.dao.get_filtered_ressources(q)

            if not result:
                return None

            ressources = [RessourceResponse(**row) for row in result]
            return ressources

        except Exception as e:
            print(f"Erreur lors de la recherche des ressources : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_ressource_by_id(self, ressource_id: int):
        try:
            result = self.dao.get_ressource_by_id(ressource_id)
            if not result:
                return None
            return RessourceResponse(**result)

        except Exception as e:
            print(f"Erreur lors de la récupération de la ressource : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_ressources_by_categorie(self, categorie_id: int):
        try:
            result = self.dao.get_ressources_by_categorie(categorie_id)
            if not result:
                return None
            return [RessourceResponse(**row) for row in result]

        except Exception as e:
            print(f"Erreur récupération ressources catégorie : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_ressources_by_auteur(self, auteur_id: int):
        try:
            result = self.dao.get_ressources_by_auteur(auteur_id)
            if not result:
                return None
            return [RessourceResponse(**row) for row in result]

        except Exception as e:
            print(f"Erreur récupération ressources auteur : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def edit_ressource(self, id: int, data: RessourceModify):
        try:
            result = self.dao.edit_ressource(id, data)
            if not result:
                return None
            return RessourceResponse(**result)

        except Exception as e:
            print(f"Erreur modification ressource : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_ressource_visibility(self, id: int, visible: bool):
        try:
            result = self.dao.update_ressource_visibility(id, visible)
            if not result:
                return None
            return RessourceResponse(**result)

        except Exception as e:
            print(f"Erreur mise à jour visibilité ressource : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete_ressource(self, id: int):
        try:
            exists = self.dao.get_ressource_by_id(id)
            if not exists:
                return None

            return self.dao.delete_ressource(id)

        except Exception as e:
            print(f"Erreur suppression ressource : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def create_ressource(self, data: RessourceCreate):
        try:
            result = self.dao.create_ressource(data)
            return result

        except Exception as e:
            print(f"Erreur création ressource : {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

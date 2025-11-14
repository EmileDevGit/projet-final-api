from data.models.model_utilisateur import UtilisateurResponse as UtilisateurResponse
from data.models.model_utilisateur import UtilisateurModify as UtilisateurModify
from fastapi import HTTPException


class UserServices:

    def __init__(self, dao):
        self.dao = dao

    def get_all_utilisateurs(self, q: str | None = None):
        try:
            if q:
                result = self.dao.get_filtered_utilisateurs(q)
            else:
                result = self.dao.get_all_utilisateurs()
            if not result:
                return None
            utilisateurs = [UtilisateurResponse(**row) for row in result]
            return utilisateurs

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

    def get_all_mentors(self):
        try:
            result = self.dao.get_all_mentors()
            if not result:
                return None
            utilisateurs = [UtilisateurResponse(**row) for row in result]
            return utilisateurs

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

    def get_utilisateur_by_id(self, utilisateur_id: int):
        try:
            result = self.dao.get_utilisateur_by_id(utilisateur_id)
            if not result:
                return None
            utilisateur = UtilisateurResponse(**result)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

    def edit_user(self, id: int, data: UtilisateurModify):
        try:
            result = self.dao.edit_user(id, data)
            if not result:
                return None
            utilisateur = UtilisateurResponse(**result)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

    def update_user_status(self, id: int, actif: bool):
        try:
            result = self.dao.update_user_status(id, actif)
            if not result:
                return None
            utilisateur = UtilisateurResponse(**result)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

    def delete_user(self, id: int):
        try:
            result = self.dao.get_utilisateur_by_id(id)
            if not result:
                return None
            return self.dao.delete_user(id)
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

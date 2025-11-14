from data.models.model_utilisateur import UtilisateurResponse as UtilisateurResponse
from data.models.model_utilisateur import UtilisateurModify as UtilisateurModify


class UserServices:

    def __init__(self, dao):
        self.dao = dao

    def get_all_utilisateurs(self, q: str | None = None):
        try:
            if q:
                result = self.dao.get_filtered_utilisateurs(q)
            else:
                result = self.dao.get_all_utilisateurs()
            utilisateurs = [UtilisateurResponse(**row) for row in result]
            return utilisateurs

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

    def get_all_mentors(self):
        try:
            result = self.dao.get_all_mentors()
            utilisateurs = [UtilisateurResponse(**row) for row in result]
            return utilisateurs

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

    def get_utilisateur_by_id(self, utilisateur_id: int):
        try:
            result = self.dao.get_utilisateur_by_id(utilisateur_id)
            utilisateur = UtilisateurResponse(**result)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return []

    def edit_user(self, id: int, data: UtilisateurModify):
        try:
            result = self.dao.edit_user(id, data)
            utilisateur = UtilisateurResponse(**result)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

    def update_user_status(self, id: int, actif: bool):
        try:
            result = self.dao.update_user_status(id, actif)
            utilisateur = UtilisateurResponse(**result)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la mise à jour du status_actif : {e}")
            return []

    def delete_user(self, id: int):
        try:
            return self.dao.delete_user(id)
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return []

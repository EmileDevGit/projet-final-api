from app.data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from fastapi import HTTPException
import bcrypt


class UtilsServices:

    def __init__(self, dao):
        self.dao = dao

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def register(self, user_data: UtilisateurCreate):
        try:
            result = self.dao.get_utilisateur_by_email(user_data.email)
            if result:
                raise HTTPException(400, detail="Cet email existe déjà")
            hashed_password = self.hash_password(user_data.mot_de_passe)
            user_data.mot_de_passe = hashed_password
            created = self.dao.create_user(user_data)
            if not created:
                raise HTTPException(
                    500, detail="Erreur interne lors de la création du compte")
            return self.dao.get_utilisateur_by_email(user_data.email)

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

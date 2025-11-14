from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from data.models.model_utilisateur import UtilisateurLogin as UtilisateurLogin
from data.models.model_utilisateur import Utilisateur as Utilisateur
from utils.auth import create_access_token
from fastapi import HTTPException


class UtilsServices:

    def __init__(self, dao):
        self.dao = dao

    def login(self, creds: UtilisateurLogin):
        try:
            result = self.dao.get_utilisateur_by_email(creds.email)
            if result is None:
                raise HTTPException(
                    status_code=401, detail="Email ou mot de passe invalide")

            user = Utilisateur(**result)

            if user.mot_de_passe != creds.mot_de_passe:
                raise HTTPException(
                    status_code=401, detail="Email ou mot de passe invalide")

            token_data = {
                "id": user.id,
                "email": user.email,
                "role": str(user.type_compte.value)
            }
            return {"token": create_access_token(token_data)}
        except Exception as e:
            print("Une erreur est survenue lors du chargement des données", e)
            return None

    def register(self, user_data: UtilisateurCreate):
        try:
            result = self.dao.get_utilisateur_by_email(user_data.email)
            if result:
                raise HTTPException(400, detail="Cet email existe déjà")
            created = self.dao.create_user(user_data)
            if not created:
                raise HTTPException(500, detail="Erreur interne lors de la création du compte")
            return self.dao.get_utilisateur_by_email(user_data.email)

        except Exception as e:
            print("Une erreur est survenue lors du chargement des données", e)
            return None

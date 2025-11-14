from data.connexion import mydb as db
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from data.models.model_utilisateur import UtilisateurResponse as UtilisateurResponse
from data.models.model_utilisateur import UtilisateurLogin as UtilisateurLogin
from data.models.model_utilisateur import Utilisateur as Utilisateur
from utils.auth import create_access_token
from fastapi import HTTPException


class UtilsServices:

    def __init__(self, db):
        self.db = db

    def login(self, creds: UtilisateurLogin):
        cursor = self.db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM utilisateur WHERE email = %s"
            cursor.execute(query, (creds.email,))
            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=401, details="Email ou mot de passe invalide")

            user = Utilisateur(**row)

            if user.mot_de_passe != creds.mot_de_passe:
                raise HTTPException(
                    status_code=401, details="Email ou mot de passe invalide")

            token_data = {
                "id": user.id,
                "email": user.email,
                "role": str(user.type_compte.value)
            }
            return {"token": create_access_token(token_data)}
        except Exception as e:
            print("Une erreur est survenue lors du chargement des données", e)
            return None
        finally:
            cursor.close()

    def register():
        return "Not Yet Implemented"

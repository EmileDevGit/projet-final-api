from data.connexion import mydb as db
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from data.models.model_utilisateur import UtilisateurResponse as UtilisateurResponse
from data.models.model_utilisateur import UtilisateurModify as UtilisateurModify


class UserServices:

    def __init__(self, db):
        self.db = db

    def get_all_utilisateurs(self, q: str | None = None):
        cursor = self.db.cursor(dictionary=True)
        try:
            if q:
                query = "SELECT * FROM utilisateur WHERE prenom LIKE %s OR nom LIKE %s"
                filter = f"%{q}%"
                cursor.execute(query, (filter, filter))
            else:
                query = "SELECT * FROM utilisateur"
                cursor.execute(query)
            result = cursor.fetchall()

            # Transformation du SET en str pour le type de compte
            for row in result:
                if isinstance(row.get("type_compte"), set):
                    row["type_compte"] = next(iter(row["type_compte"]), "USER")

            utilisateurs = [UtilisateurResponse(**row) for row in result]

            return utilisateurs

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

        finally:
            cursor.close()

    def get_all_mentors(self):
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM utilisateur WHERE type_compte = 'MENTOR'")
            result = cursor.fetchall()

            # Transformation du SET en str pour le type de compte
            for row in result:
                if isinstance(row.get("type_compte"), set):
                    row["type_compte"] = next(iter(row["type_compte"]), "USER")

            utilisateurs = [UtilisateurResponse(**row) for row in result]

            return utilisateurs

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

        finally:
            cursor.close()

    def get_utilisateur_by_id(self, utilisateur_id: int):
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM utilisateur WHERE utilisateur_id = {utilisateur_id}")
            row = cursor.fetchone()
            if isinstance(row.get("type_compte"), set):
                row["type_compte"] = next(iter(row["type_compte"]), "USER")

            utilisateur = UtilisateurResponse(**row)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None

        finally:
            cursor.close()

    def edit_user(self, id: int, data: UtilisateurModify):
        cursor = self.db.cursor(dictionary=True)
        try:
            query = "UPDATE utilisateur SET nom=%s, prenom=%s, email=%s, mot_de_passe=%s WHERE utilisateur_id=%s"
            values = [data.nom, data.prenom,
                      data.email, data.mot_de_passe, id]
            cursor.execute(query, values)

        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return
        finally:
            cursor.close()

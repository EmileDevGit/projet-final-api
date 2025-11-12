from data.connexion import mydb as db
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate
from data.models.model_utilisateur import UtilisateurResponse as UtilisateurResponse


class UserServices:

    def __init__(self, db):
        self.db = db

    def get_all_utilisateurs(self):
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM utilisateur")
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
            cursor.execute("SELECT * FROM utilisateur WHERE utilisateur_id = %s", (utilisateur_id,))
            row = cursor.fetchone()
            # Transformation du SET en str pour le type de compte
            if isinstance(row.get("type_compte"), set):
                row["type_compte"] = next(iter(row["type_compte"]), "USER")

            utilisateur = UtilisateurResponse(**row)
            return utilisateur

        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None

        finally:
            cursor.close()


from data.dao.I_dao_utilisateur import IUtilisateurDAO
from data.models.model_utilisateur import UtilisateurModify as UtilisateurModify
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate


class UtilisateurDAO(IUtilisateurDAO):

    def __init__(self, db):
        self.db = db

    def get_all_utilisateurs(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM utilisateur
                """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_filtered_utilisateurs(self, q: str):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM utilisateur
                WHERE nom LIKE %s
                OR prenom LIKE %s
                """
        pattern = f"%{q}%"
        cursor.execute(query, (pattern, pattern))
        result = cursor.fetchall()
        return result

    def get_all_mentors(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM utilisateur
                WHERE type_compte = 'MENTOR'
                """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_filtered_mentors(self, q: str):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM utilisateur
                WHERE type_compte = 'MENTOR'
                AND (
                    nom LIKE %s
                    OR prenom LIKE %s
                )
                """
        pattern = f"%{q}%"
        cursor.execute(query, (pattern, pattern))
        result = cursor.fetchall()
        return result

    def get_utilisateur_by_id(self, id: int):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM utilisateur
                WHERE utilisateur_id = %s
                """
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result

    def get_utilisateur_by_email(self, email: str):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM utilisateur
                WHERE email = %s
                """
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def edit_user(self, id: int, user_data: UtilisateurModify):
        cursor = self.db.cursor(dictionary=True)
        query = """
                UPDATE utilisateur
                SET nom = %s, prenom = %s, email = %s, mot_de_passe = %s
                WHERE utilisateur_id = %s
                """
        values = [
            user_data.nom,
            user_data.prenom,
            user_data.email,
            user_data.mot_de_passe,
            id
        ]
        cursor.execute(query, values)
        self.db.commit()
        return self.get_utilisateur_by_id(id)

    def delete_user(self, id: int):
        cursor = self.db.cursor(dictionary=True)
        query = """
                DELETE
                FROM utilisateur
                WHERE utilisateur_id = %s
                """
        cursor.execute(query, (id,))
        self.db.commit()
        return True

    def update_user_status(self, id: int, actif: bool):
        cursor = self.db.cursor(dictionary=True)
        query = """
                UPDATE utilisateur
                SET status_actif = %s
                WHERE utilisateur_id = %s
                """
        values = [
            actif,
            id
        ]
        cursor.execute(query, values)
        self.db.commit()
        return self.get_utilisateur_by_id(id)

    def create_user(self, user_data: UtilisateurCreate):
        cursor = self.db.cursor(dictionary=True)
        query = """
                INSERT
                INTO utilisateur(
                    nom,
                    prenom,
                    email,
                    mot_de_passe,
                    status_actif,
                    type_compte
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        values = [
            user_data.nom,
            user_data.prenom,
            user_data.email,
            user_data.mot_de_passe,
            True,
            user_data.type_compte
        ]
        cursor.execute(query, values)
        self.db.commit()
        return True

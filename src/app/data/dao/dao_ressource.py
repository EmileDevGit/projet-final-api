from data.dao.I_dao_ressource import IRessourceDAO
from data.models.model_ressource import RessourceModify, RessourceCreate

class RessourceDAO(IRessourceDAO):

    def __init__(self, db):
        self.db = db

    def get_all_ressources(self):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM ressource
                """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_filtered_ressources(self, q: str):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM ressource
                WHERE titre LIKE %s
                """
        pattern = f"%{q}%"
        cursor.execute(query, (pattern, pattern))
        result = cursor.fetchall()
        return result

    def get_ressource_by_id(self, id: int):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM ressource
                WHERE ressource_id = %s
                """
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def get_ressources_by_categorie(self, categorie_id: int):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM ressource
                WHERE categorie_id = %s
                """
        cursor.execute(query, (categorie_id,))
        return cursor.fetchall()

    def get_ressources_by_auteur(self, auteur_id: int):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM ressource
                WHERE auteur_id = %s
                """
        cursor.execute(query, (auteur_id,))
        return cursor.fetchall()

    def edit_ressource(self, id: int, res_data: RessourceModify):
        cursor = self.db.cursor(dictionary=True)
        query = """
                UPDATE ressource
                SET titre = %s,
                    description = %s,
                    url_ressource = %s,
                    visibilite = %s,
                    categorie_id = %s
                WHERE ressource_id = %s
                """
        values = [
            res_data.titre,
            res_data.description,
            res_data.url_ressource,
            res_data.visibilite,
            res_data.categorie_id,
            id
        ]
        cursor.execute(query, values)
        self.db.commit()
        return self.get_ressource_by_id(id)

    def delete_ressource(self, id: int):
        cursor = self.db.cursor(dictionary=True)
        query = """
                DELETE FROM ressource
                WHERE ressource_id = %s
                """
        cursor.execute(query, (id,))
        self.db.commit()
        return True

    def update_ressource_visibility(self, id: int, visible: bool):
        cursor = self.db.cursor(dictionary=True)
        query = """
                UPDATE ressource
                SET visibilite = %s
                WHERE ressource_id = %s
                """
        cursor.execute(query, (visible, id))
        self.db.commit()
        return self.get_ressource_by_id(id)

    def create_ressource(self, res_data: RessourceCreate):
        cursor = self.db.cursor(dictionary=True)
        query = """
                INSERT INTO ressource(
                    titre,
                    description,
                    url_ressource,
                    visibilite,
                    categorie_id,
                    auteur_id
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        values = [
            res_data.titre,
            res_data.description,
            res_data.url_ressource,
            True,
            res_data.categorie_id,
            res_data.auteur_id
        ]
        cursor.execute(query, values)
        self.db.commit()
        return True
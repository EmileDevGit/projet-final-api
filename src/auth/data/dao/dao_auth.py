from auth.data.dao.I_dao_auth import IAuthDAO
from mysql.connector import Error as MySQLError


class TokenDatabaseError(Exception):
    pass


class AuthDAO(IAuthDAO):
    def __init__(self, db):
        self.db = db

    def check_refresh_token(self, jwt_id: str):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT *
                    FROM refresh_token
                    WHERE jwt_id = %s
                    """
            cursor.execute(query, (jwt_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except MySQLError as e:
            if cursor:
                cursor.close()
            raise TokenDatabaseError(f"Erreur de la base de donnees lors de la verification du token: {e}")
        except Exception as e:
            if cursor:
                cursor.close()
            raise TokenDatabaseError(f"Erreur innatendue lors de la verification du token: {e}")

    def save_refresh_token(self, token_data: dict):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    INSERT INTO refresh_token(
                        jwt_id,
                        user_sub,
                        expires_at)
                    VALUES (%s, %s, %s)
                    """
            values = [
                token_data["jwt_id"],
                token_data["sub"],
                token_data["exp"]
            ]
            cursor.execute(query, values)
            self.db.commit()
            cursor.close()
            return True
        except MySQLError as e:
            if cursor:
                cursor.close()
            self.db.rollback()
            raise TokenDatabaseError(f"Erreur de la base de donnees lors de la sauvegarde du token de rafraichissement: {e}")
        except Exception as e:
            if cursor:
                cursor.close()
            self.db.rollback()
            raise TokenDatabaseError(f"Erreur innatendue lors de la sauvegarde du token de rafraichissement: {e}")

    def update_refresh_token_state(self, jwt_id: str, is_revoked: bool):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    UPDATE refresh_token
                    SET is_revoked = %s
                    WHERE jwt_id = %s
                    """
            cursor.execute(query, (is_revoked, jwt_id))
            self.db.commit()
            cursor.close()
            return True
        except MySQLError as e:
            if cursor:
                cursor.close()
            self.db.rollback()
            raise TokenDatabaseError(f"Erreur de la base de donnees lors de l'invalidation du token de rafraichissement: {e}")
        except Exception as e:
            if cursor:
                cursor.close()
            self.db.rollback()
            raise TokenDatabaseError(f"Erreur innatendue lors de l'invalidation du token de refraichissement: {e}")

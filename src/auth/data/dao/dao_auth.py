from auth.data.dao.I_dao_auth import IAuthDAO
from datetime import datetime


class AuthDAO(IAuthDAO):

    def __init__(self, db):
        self.db = db

    def check_refresh_token(self, jwt_id: str):
        cursor = self.db.cursor(dictionary=True)
        query = """
                SELECT *
                FROM refresh_token
                WHERE jwt_id = %s
                """
        cursor.execute(query, (jwt_id,))
        result = cursor.fetchone()
        return result

    def save_refresh_token(self, token_data: dict):
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
        return True

    def update_refresh_token_state(self, jwt_id: str, is_revoked: bool):
        cursor = self.db.cursor(dictionary=True)
        query = """
                UPDATE refresh_token
                SET is_revoked = %s
                WHERE jwt_id = %s
                """
        cursor.execute(query, (is_revoked, jwt_id))
        self.db.commit()
        return True

    def create_refresh_token(self, res_data: dict):
        pass

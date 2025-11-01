from pydantic import BaseModel, Field
from data.connexion import mydb as db
from data.models.model_utilisateur import Utilisateur as Utilisateur


class ListUser(BaseModel):
    users: list[Utilisateur] = Field(default_factory=list)


class UserServices:

    def __init__(self, db):
        self.db = db

    def get_all_utilisateurs(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateur")
        result = cursor.fetchall()
        cursor.close()

        utilisateurs = [Utilisateur(**user) for user in result]
        return ListUser(users=utilisateurs).model_dump()

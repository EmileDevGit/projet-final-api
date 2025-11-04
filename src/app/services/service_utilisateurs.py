from data.connexion import mydb as db


class UserServices:

    def __init__(self, db):
        self.db = db

    def get_all_utilisateurs(self):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateur")
        myresult = cursor.fetchall()
        return myresult

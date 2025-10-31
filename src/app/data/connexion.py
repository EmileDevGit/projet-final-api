import mysql.connector
from config.env import settings as settings

mydb = mysql.connector.connect(
    host=settings.DATABASE_HOST,
    database=settings.MYSQL_DATABASE,
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD
)

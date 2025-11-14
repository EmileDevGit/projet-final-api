from fastapi import FastAPI
from routers.router_utilisateurs import users_router as utilisateurs
from routers.router_utils import utils_router as utils
from data.connexion import mydb as mydb
app = FastAPI()
app.include_router(utilisateurs)
app.include_router(utils)


@app.get("/health")
def check_service_health():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Bonjour, bienvenue sur Sapienta!"}


@app.get("/db-status")
def check_db_health():
    conn = mydb
    if conn.is_connected():
        conn.close()
        return {"status": "ok", "database_connection": "successful"}

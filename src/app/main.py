from fastapi import FastAPI
from app.routers.router_utilisateurs import users_router as utilisateurs
from app.routers.router_ressources import ressources_router
from app.routers.router_utils import utils_router as utils
from app.data.connexion import mydb as mydb
app = FastAPI(
    title="SapientAPI",
    version="0.9.0",
    description="SapientaAPI est une API conçue pour centraliser, " \
    "organiser et partager des ressources pédagogiques. " \
    "Elle permet de créer une véritable bibliothèque de savoir, " \
    "structurée en collections et en différents types de documents. " \
    "La plateforme gère les membres, leurs rôles et leurs ressources " \
    ": les mentors peuvent publier et organiser du contenu tout en contrôlant sa visibilité, " \
    "tandis que les utilisateurs peuvent consulter les ressources disponibles " \
    "et conserver leurs propres notes personnelles. " \
    "SapientaAPI simplifie ainsi la gestion et la diffusion de connaissances numériques."
)
app.include_router(utilisateurs)
app.include_router(ressources_router)
app.include_router(utils)


@app.get("/health", tags=["Utils"])
def check_service_health():
    return {"status": "ok"}


@app.get("/", tags=["Utils"])
def read_root():
    return {"message": "Bonjour, bienvenue sur Sapienta!"}


@app.get("/db-status", tags=["Utils"])
def check_db_health():
    conn = mydb
    if conn.is_connected():
        conn.close()
        return {"status": "ok", "database_connection": "successful"}


print("Routes enregistrées :")
for route in app.routes:
    print(route.path)

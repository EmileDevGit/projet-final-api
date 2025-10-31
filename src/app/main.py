from fastapi import FastAPI
from routers.router_utilisateurs import users_router as utilisateurs
app = FastAPI()
app.include_router(utilisateurs)


@app.get("/health")
def check_service_health():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Bonjour, bienvenue sur Sapienta!"}

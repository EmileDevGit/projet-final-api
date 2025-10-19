from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def check_service_health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Bonjour, bienvenue sur Sapienta!"}


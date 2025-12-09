from fastapi import FastAPI

from auth.config.env import settings
from auth.interface.routers import router_auth

auth = FastAPI(
    title=settings.AUTH_PROJECT_NAME,
    version=settings.AUTH_API_VERSION
)


@auth.get("/")
def root():
    return {"message": "Bonjour, AUTH!"}


auth.include_router(router_auth.router)


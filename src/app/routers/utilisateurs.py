from fastApi import APIRouter

users_router = APIRouter(prefix="/utilisateurs")

@users_router.get("/")
async def get_users():
    return { "message": "Une liste d'utilisateurs" }

@users_router.get("/{id}")
async def get_user_by_id(id: int):
    return { "message": "Un utilisateurs particulier" }

@users_router.patch("/{id}")
async def patch_user_visibility(id: int, actif: bool):
    return { "message": f"L'utilisateur avec l'id {id} est mis à jour actif: {actif}" }

@users_router.post("/")
async def post_users():
    return { "message": "Création d'un utilisateur" }






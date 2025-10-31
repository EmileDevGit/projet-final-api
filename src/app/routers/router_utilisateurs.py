from fastapi import APIRouter

users_router = APIRouter(prefix="/utilisateurs")

# ====== GET ====== #
@users_router.get("/")
async def get_users():
    return { "message": "Une liste d'utilisateurs" }

@users_router.get("/{id}")
async def get_user_by_id(id: int):
    return { "message": "Un utilisateurs particulier" }


# ====== POST ======= #
@users_router.post("/")
async def post_users():
    return { "message": "Création d'un utilisateur" }


# ====== PUT ======= #
@users_router.put("/{id}")
async def put_user(id: int):
    return { "message": "Modification d'un utilisateur" }

# ====== PATCH ====== #
@users_router.patch("/{id}")
async def patch_user_visibility(id: int, actif: bool):
    return { "message": f"L'utilisateur avec l'id {id} est mis à jour actif: {actif}" }

# ====== DELETE ====== #
@users_router.delete("/{id}")
async def delete_user(id: int):
    return { "message": f"L'utilisateur avec l'id {id} à été supprimé" }






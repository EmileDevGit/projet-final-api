from fastapi import APIRouter, Depends, HTTPException
from app.data.connexion import mydb as db
from app.data.dao.dao_utilisateur import UtilisateurDAO as UtilisateurDAO
from app.services.service_utilisateurs import UserServices as UserServices
from app.utils.auth import verify_token
from app.data.models.model_utilisateur import UtilisateurModify as UtilisateurModify

# Gestion des dépendances
users_router = APIRouter(prefix="/utilisateurs")


def get_dao():
    return UtilisateurDAO(db)


def get_service(dao: UtilisateurDAO = Depends(get_dao)):
    return UserServices(dao)


# Routes Utilisateurs
@users_router.get("/")
async def get_users(
        q: str | None = None,
        user: dict = Depends(verify_token),
        service: UserServices = Depends(get_service)):
    if user["role"] == "ADMIN":
        return service.get_all_utilisateurs(q)
    else:
        return service.get_all_mentors()


@users_router.get("/{id}")
async def get_user_by_id(
        id: int,
        user: dict = Depends(verify_token),
        service: UserServices = Depends(get_service)):
    if user["role"] == "ADMIN" or user["id"] == id:
        utilisateur = service.get_utilisateur_by_id(id)
        if not utilisateur:
            raise HTTPException(
                status_code=404, detail="Utilisateur non trouvé")
        return utilisateur
    else:
        raise HTTPException(
            status_code=403, detail="Accès refusé : vous ne pouvez consulter que votre propre profil")


@users_router.put("/{id}")
async def put_user(
        id: int, data: UtilisateurModify,
        user: dict = Depends(verify_token),
        service: UserServices = Depends(get_service)):
    if user["role"] == "ADMIN" or user["id"] == id:
        return service.edit_user(id, data)
    else:
        raise HTTPException(
            status_code=403, detail="Vous ne possédez pas les droits de modification pour cet utilisateur")


@users_router.patch("/{id}")
async def patch_user_visibility(
        id: int, actif: bool,
        user=Depends(verify_token),
        service: UserServices = Depends(get_service)):
    if user["role"] == "ADMIN" or user["id"] == id:
        updated_user = service.update_user_status(id, actif)
        if not updated_user:
            raise HTTPException(
                status_code=404, detail="Utilisateur non trouvé")
        return updated_user

    else:
        raise HTTPException(
            status_code=403,
            detail="Vous ne possédez pas les droits de modification pour cet utilisateur"
        )


@users_router.delete("/{id}")
async def delete_user(
        id: int,
        user: dict = Depends(verify_token),
        service: UserServices = Depends(get_service)):
    if user["role"] == "ADMIN" or user["id"] == id:
        deleted_user = service.delete_user(id)
        if not deleted_user:
            raise HTTPException(
                status_code=404, detail="Utilisateur non trouvé")
        return {"message": f"L'utilisateur avec l'id {id} a été supprimé avec succès"}
    else:
        raise HTTPException(
            status_code=403, detail="Vous ne possédez pas les droits de suppression pour cet utilisateur")

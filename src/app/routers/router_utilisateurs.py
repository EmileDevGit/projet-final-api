from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.data.connexion import mydb as db
from app.data.dao.dao_utilisateur import UtilisateurDAO
from app.services.service_utilisateurs import UserServices
from app.services.service_auth import AuthServices
from app.interface.model_view.model_view_token_decoded import TokenViewDecoded
from app.data.models.model_utilisateur import UtilisateurModify

# Gestion des dépendances
users_router = APIRouter(prefix="/utilisateurs")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_dao():
    return UtilisateurDAO(db)


def get_service(dao: UtilisateurDAO = Depends(get_dao)):
    return UserServices(dao)


def get_auth_service(dao: UtilisateurDAO = Depends(get_dao)):
    return AuthServices(dao)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthServices = Depends(get_auth_service)
):
    try:
        token_decoded = auth_service.validate_token(token)
        print(f"TOKEN DECODED: {token_decoded}")
        return token_decoded
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


# Routes Utilisateurs
@users_router.get("/", tags=["Utilisateurs"], summary="Récupérer la liste des utilisateurs", description="")
async def get_users(
        q: str | None = None,
        user_token: TokenViewDecoded = Depends(get_current_user),
        service: UserServices = Depends(get_service)):
    if user_token.role == "ADMIN":
        return service.get_all_utilisateurs(q)
    else:
        return service.get_all_mentors()


@users_router.get("/{id}", tags=["Utilisateurs"], summary="Récupérer un utilisateur", description="")
async def get_user_by_id(
        id: int,
        user_token: TokenViewDecoded = Depends(get_current_user),
        service: UserServices = Depends(get_service)):
    if user_token.role == "ADMIN" or user_token.id == id:
        utilisateur = service.get_utilisateur_by_id(id)
        if not utilisateur:
            raise HTTPException(
                status_code=404, detail="Utilisateur non trouvé")
        return utilisateur
    else:
        raise HTTPException(
            status_code=403, detail="Accès refusé : vous ne pouvez consulter que votre propre profil")


@users_router.put("/{id}", tags=["Utilisateurs"], summary="Modifier un utilisateur", description="")
async def put_user(
        id: int, data: UtilisateurModify,
        user_token: TokenViewDecoded = Depends(get_current_user),
        service: UserServices = Depends(get_service)):
    if user_token.role == "ADMIN" or user_token.id == id:
        return service.edit_user(id, data)
    else:
        raise HTTPException(
            status_code=403, detail="Vous ne possédez pas les droits de modification pour cet utilisateur")


@users_router.patch("/{id}", tags=["Utilisateurs"], summary="Modifier la visibilié d'un utilisateur", description="")
async def patch_user_visibility(
        id: int, actif: bool,
        user_token: TokenViewDecoded = Depends(get_current_user),
        service: UserServices = Depends(get_service)):
    if user_token.role == "ADMIN" or user_token.id == id:
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


@users_router.delete("/{id}", tags=["Utilisateurs"], summary="Supprimer un utilisateur", description="")
async def delete_user(
        id: int,
        user_token: TokenViewDecoded = Depends(get_current_user),
        service: UserServices = Depends(get_service)):
    if user_token.role == "ADMIN" or user_token.id == id:
        deleted_user = service.delete_user(id)
        if not deleted_user:
            raise HTTPException(
                status_code=404, detail="Utilisateur non trouvé")
        return {"message": f"L'utilisateur avec l'id {id} a été supprimé avec succès"}
    else:
        raise HTTPException(
            status_code=403, detail="Vous ne possédez pas les droits de suppression pour cet utilisateur")

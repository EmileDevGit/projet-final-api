from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.data.connexion import mydb as db
from app.data.dao.dao_ressource import RessourceDAO
from app.data.dao.dao_utilisateur import UtilisateurDAO
from app.services.service_ressource import RessourceService
from app.services.service_auth import AuthServices
from app.interface.model_view.model_view_token_decoded import TokenViewDecoded
from app.data.models.model_ressource import RessourceModify, RessourceCreate
print(">>> Chargement router_ressources")


ressources_router = APIRouter(prefix="/ressources")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_ressource_dao():
    return RessourceDAO(db)


def get_utilisateur_dao():
    return UtilisateurDAO(db)


def get_service(dao: RessourceDAO = Depends(get_ressource_dao)):
    return RessourceService(dao)


def get_auth_service(dao: UtilisateurDAO = Depends(get_utilisateur_dao)):
    return AuthServices(dao)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthServices = Depends(get_auth_service)
):
    try:
        token_decoded = auth_service.validate_token(token)
        return token_decoded
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@ressources_router.get("/", tags=["Ressources"], summary="Récupérer la liste des ressources",     description=(
        "Droits d'accès :\n"
        "- **Utilisateur** : peut lister toutes les ressources **publiques** et ses "
        "propres ressources (publiques ou privées).\n"
        "- **Mentor** : peut lister toutes les ressources **publiques** et ses "
        "propres ressources (publiques ou privées).\n"
        "- **Admin** : peut lister **toutes** les ressources, quelle que soit leur "
        "visibilité ou leur auteur."
    ))
async def get_ressources(
    q: str | None = None,
    user_token: TokenViewDecoded = Depends(get_current_user),
    service: RessourceService = Depends(get_service)
):
    ressources = service.get_all_ressources(q) or []

    role = user_token.role
    user_id = user_token.id

    if role == "ADMIN":
        return ressources

    return [r for r in ressources if r.visibilite or r.auteur_id == user_id]


@ressources_router.get("/{id}", tags=["Ressources"], summary="Récupérer une ressource",     description=(
        "Droits d'accès :\n"
        "- **Utilisateur** : peut consulter une ressource si elle est **publique** "
        "ou si c’est l’une de ses propres ressources.\n"
        "- **Mentor** : mêmes droits que l’utilisateur (ressources publiques ou "
        "propres).\n"
        "- **Admin** : peut consulter **toutes** les ressources."
    ))
async def get_ressource_by_id(
    id: int,
    user_token: TokenViewDecoded = Depends(get_current_user),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user_token.role
    user_id = user_token.id

    if role == "ADMIN":
        return res

    if res.visibilite or res.auteur_id == user_id:
        return res

    raise HTTPException(
        403, "Accès refusé : vous ne pouvez consulter que vos propre ressouces")


@ressources_router.post("/", tags=["Ressources"], summary="Créer une nouvelle ressource",     description=(
        "Droits d'accès :\n"
        "- **Utilisateur** : peut créer uniquement des ressources **privées** dont "
        "il est automatiquement l’auteur (visibilité forcée à privée).\n"
        "- **Mentor** : peut créer des ressources **publiques ou privées** dont il "
        "est automatiquement l’auteur.\n"
        "- **Admin** : peut créer des ressources **publiques ou privées** pour "
        "n’importe quel utilisateur."
    ))
async def create_ressource(
    data: RessourceCreate,
    user_token: TokenViewDecoded = Depends(get_current_user),
    service: RessourceService = Depends(get_service)
):
    role = user_token.role

    if role == "ADMIN":
        return service.create_ressource(data)

    if role == "MENTOR":
        data.auteur_id = user_token["id"]
        return service.create_ressource(data)

    if role == "USER":
        data.visibilite = False
        data.auteur_id = user_token["id"]
        return service.create_ressource(data)

    raise HTTPException(403, "Accès interdit")


@ressources_router.put("/{id}", tags=["Ressources"], summary="Modifier une ressource", description=(
        "Droits d'accès :\n"
        "- **Utilisateur** : peut modifier uniquement ses **propres** ressources.\n"
        "- **Mentor** : peut modifier uniquement ses **propres** ressources.\n"
        "- **Admin** : peut modifier **toutes** les ressources."
    ))
async def update_ressource(
    id: int,
    data: RessourceModify,
    user_token: TokenViewDecoded = Depends(get_current_user),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user_token.role
    user_id = user_token.id

    if role == "ADMIN":
        return service.edit_ressource(id, data)

    if res.auteur_id == user_id:
        return service.edit_ressource(id, data)

    raise HTTPException(
        403, "Vous ne pouvez modifier que vos propres ressources")


@ressources_router.patch("/{id}", tags=["Ressources"], summary="Modifier la visibilité d'une ressoruce",     description=(
        "Droits d'accès :\n"
        "- **Utilisateur** : peut changer la visibilité uniquement de ses "
        "**propres** ressources.\n"
        "- **Mentor** : peut changer la visibilité uniquement de ses **propres** "
        "ressources.\n"
        "- **Admin** : peut changer la visibilité de **toutes** les ressources."
    ))
async def update_visibility(
    id: int,
    visible: bool,
    user_token: TokenViewDecoded = Depends(get_current_user),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user_token.role
    user_id = user_token.id

    if role == "ADMIN":
        return service.update_ressource_visibility(id, visible)

    if res.auteur_id == user_id:
        return service.update_ressource_visibility(id, visible)

    raise HTTPException(
        403, "Vous ne pouvez modifier que vos propres ressources")


@ressources_router.delete("/{id}", tags=["Ressources"], summary="Supprimer une ressource",     description=(
        "Droits d'accès :\n"
        "- **Utilisateur** : peut supprimer uniquement ses **propres** ressources.\n"
        "- **Mentor** : peut supprimer uniquement ses **propres** ressources.\n"
        "- **Admin** : peut supprimer **toutes** les ressources."
    ))
async def delete_ressource(
    id: int,
    user_token: TokenViewDecoded = Depends(get_current_user),
    service: RessourceService = Depends(get_service)
):
    res = service.get_ressource_by_id(id)
    if not res:
        raise HTTPException(404, "Ressource non trouvée")

    role = user_token.role
    user_id = user_token.id

    if role == "ADMIN":
        service.delete_ressource(id)
        return {"message": "Ressource supprimée avec succès"}

    if res.auteur_id == user_id:
        service.delete_ressource(id)
        return {"message": "Ressource supprimée avec succès"}

    raise HTTPException(
        403, "Vous ne pouvez supprimer que vos propres ressources")

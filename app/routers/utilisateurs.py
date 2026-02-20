from fastapi import APIRouter, Depends, Body, Query, Path, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from typing import List, Annotated
from datetime import timedelta


from app.core.session import Session, get_session
from app.core.security import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

from app.core.dependencies import requires_role

from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import (
    UtilisateurCreate,
    UtilisateurRead,
    UtilisateurUpdate,
    Token,
)
from app.services.utilisateurs import (
    authentificate_user,
    create_utilisateur,
    read_utilisateurs,
    read_utilisateur,
    update_utilisateur,
    delete_utilisateur,
)


router = APIRouter(prefix="/api/utilisateurs", tags=["Utilisateurs"])

ROLES_ADMIN_AGRICULTEUR = ["Admin", "Agriculteur"]
ROLES_ALL = ["Admin", "Agriculteur", "Technicien"]
ROLES_ADMIN_TECHNICIEN = ["Admin", "Technicien"]
not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur inexistant"
)


def forbiden_error(message):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)


@router.post("/token")
async def login_for_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    utilisateur = authentificate_user(session, form_data.username, form_data.password)
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": utilisateur.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UtilisateurRead)
async def read_utilisateurs_me(
    utilisateur_current: Annotated[Utilisateur, Depends(requires_role(*ROLES_ALL))],
):

    return utilisateur_current


@router.post("/", response_model=UtilisateurRead)
async def create_utilisateur_endpoint(
    session: Session = Depends(get_session), utilisateur: UtilisateurCreate = Body(...)
):
    return create_utilisateur(session=session, utilisateur=utilisateur)


@router.get("/", response_model=List[UtilisateurRead])
async def read_utilisateurs_endpoint(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_TECHNICIEN)),
):
    if utilisateur_current.role not in ROLES_ADMIN_TECHNICIEN:
        raise forbiden_error(
            "Vous n'avez pas les droits\
                             pour voir les utilisateurs"
        )

    return read_utilisateurs(session=session, offset=offset, limit=limit)


@router.get("/{utilisateur_id}", response_model=UtilisateurRead)
async def read_utilisateur_endpoint(
    session: Session = Depends(get_session),
    utilisateur_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL)),
):
    if (
        utilisateur_current.id != utilisateur_id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error(
            "Vous n'avez pas les droits\
        pour voir l'utilisateur"
        )

    utilisateur = read_utilisateur(session=session, utilisateur_id=utilisateur_id)
    if not utilisateur:
        raise not_found_error
    return utilisateur


@router.put("/{utilisateur_id}", response_model=UtilisateurRead)
async def update_utilisateur_endpoint(
    session: Session = Depends(get_session),
    utilisateur_id: int = Path(...),
    utilisateur: UtilisateurUpdate = Body(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL)),
):

    if (
        utilisateur_current.id != utilisateur_id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error(
            "Vous n'avez pas les droits\
                             pour modifier l'utilisateur"
        )

    utilisateur = update_utilisateur(
        session=session, utilisateur_id=utilisateur_id, utilisateur=utilisateur
    )
    if not utilisateur:
        raise not_found_error
    return utilisateur


@router.delete("/{utilisateur_id}", response_model=UtilisateurRead)
async def delete_utilisateur_endpoint(
    session: Session = Depends(get_session),
    utilisateur_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR)),
):
    if (
        utilisateur_current.id != utilisateur_id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error(
            "Vous n'avez pas les droits\
                             pour supprimer l'utilisateur"
        )

    utilisateur = delete_utilisateur(session=session, utilisateur_id=utilisateur_id)
    if not utilisateur:
        raise not_found_error
    return utilisateur

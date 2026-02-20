from fastapi import APIRouter, Depends, Body, Query, Path, HTTPException, status
from typing import List
from app.core.session import Session, get_session
from app.core.dependencies import requires_role
from app.models.utilisateur import Utilisateur
from app.schemas.ferme import FermeCreate, FermeRead, FermeUpdate
from app.services.fermes import (
    create_ferme,
    read_fermes,
    read_ferme,
    read_ferme_by_utilisateur,
    update_ferme,
    delete_ferme,
)


router = APIRouter(prefix="/api/fermes", tags=["Fermes"])

ROLES_ADMIN_AGRICULTEUR = ["Admin", "Agriculteur"]
ROLES_ALL = ["Admin", "Agriculteur", "Technicien"]
not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Ferme inexistante"
)


def forbiden_error(message):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)


@router.post("/", response_model=FermeRead)
def create_ferme_endpoint(
    session: Session = Depends(get_session),
    ferme: FermeCreate = Body(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR)),
):
    if (
        utilisateur_current.role == "Agriculteur"
        and utilisateur_current.id != ferme.utilisateur_id
    ):
        raise forbiden_error(
            "Vous ne pouvez créer une ferme\
                             que pour votre propre compte"
        )

    return create_ferme(
        session=session, ferme=ferme, utilisateur_current=utilisateur_current
    )


@router.get("/", response_model=List[FermeRead])
async def read_fermes_endpoint(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(100, le=100),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL)),
):
    if utilisateur_current.role == "Agriculteur":
        return read_ferme_by_utilisateur(
            session=session, utilisateur_id=utilisateur_current.id
        )
    return read_fermes(session=session, offset=offset, limit=limit)


@router.get("/{ferme_id}", response_model=FermeRead)
async def read_ferme_endpoint(
    session: Session = Depends(get_session),
    ferme_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL)),
):
    ferme = read_ferme(session=session, ferme_id=ferme_id)

    if not ferme:
        raise not_found_error
    if (
        ferme.utilisateur_id != utilisateur_current.id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error("Vous n'avez pas les droits pour voir la ferme")

    return ferme


@router.get("/utilisateur/{utilisateur_id}", response_model=List[FermeRead])
async def read_fermes_by_utilisateur_endpoint(
    session: Session = Depends(get_session),
    utilisateur_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL)),
):
    if (
        utilisateur_current.id != utilisateur_id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error(
            "Vous n'avez pas les droits pour\
                             voir les fermes de cet utilisateur"
        )
    fermes = read_ferme_by_utilisateur(session=session, utilisateur_id=utilisateur_id)
    if not fermes:
        raise not_found_error

    return fermes


@router.put("/{ferme_id}", response_model=FermeRead)
async def update_ferme_endpoint(
    session: Session = Depends(get_session),
    ferme_id: int = Path(...),
    ferme_data: FermeUpdate = Body(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR)),
):
    ferme = read_ferme(session=session, ferme_id=ferme_id)

    if not ferme:
        raise not_found_error

    if (
        utilisateur_current.id != ferme.utilisateur_id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error(
            "Vous n'avez pas les droits\
                             pour modifier la ferme"
        )

    ferme = update_ferme(session=session, ferme_id=ferme_id, ferme=ferme_data)

    return ferme


@router.delete("/{ferme_id}", response_model=FermeRead)
async def delete_ferme_endpoint(
    session: Session = Depends(get_session),
    ferme_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR)),
):
    ferme = read_ferme(session=session, ferme_id=ferme_id)

    if not ferme:
        raise not_found_error

    if (
        utilisateur_current.id != ferme.utilisateur_id
        and utilisateur_current.role == "Agriculteur"
    ):
        raise forbiden_error(
            "Vous n'avez pas les droits\
                             pour supprimer la ferme"
        )

    ferme = delete_ferme(session=session, ferme_id=ferme_id)

    return ferme

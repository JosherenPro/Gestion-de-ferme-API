from fastapi import APIRouter, Depends, Body, Query, Path, HTTPException, status
from typing import List
from app.core.session import Session, get_session
from app.schemas.culture import (
    CultureCreate,
    CultureRead,
    CultureUpdate
)
from app.core.dependencies import requires_role
from app.schemas.culture import CultureCreate, CultureRead, CultureUpdate
from app.models.utilisateur import Utilisateur
from app.services.cultures import (
    create_culture,
    read_cultures,
    read_culture,
    read_cultures_by_utilisateur,
    read_cultures_by_ferme,
    update_culture,
    delete_culture
)



router = APIRouter(prefix="/api/cultures", tags=["Cultures"])

ROLES_ADMIN_AGRICULTEUR = ["Admin", "Agriculteur"]
ROLES_ALL = ["Admin", "Agriculteur", "Technicien"]


@router.post("/", response_model=CultureRead)
def create_culture_endpoint(
    session: Session = Depends(get_session),
    culture: CultureCreate = Body(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR))
):
    if utilisateur_current.id != culture.utilisateur_id and utilisateur_current.role == "Agriculteur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les permissions nécessaires pour créer une culture pour cet utilisateur"
        )
    return create_culture(session=session, culture_data=culture, utilisateur_current=utilisateur_current)


@router.get("/", response_model=List[CultureRead])
async def read_cultures_endpoint(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(100, le=100),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL))
):
    if utilisateur_current.role == "Agriculteur":
        return read_cultures_by_utilisateur(session=session, utilisateur_id=utilisateur_current.id)
    cultures = read_cultures(session=session, offset=offset, limit=limit)
    return cultures


@router.get("/{culture_id}", response_model=CultureRead)
async def read_culture_endpoint(
    session: Session = Depends(get_session),
    culture_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL))
):
    culture = read_culture(session=session, culture_id=culture_id)

    if not culture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Culture inexistante"
        )
    
    if culture.utilisateur_id != utilisateur_current.id and utilisateur_current.role == "Agriculteur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les permissions nécessaires pour voir cette culture"
        )

    return culture


@router.get("/utilisateur/{utilisateur_id}", response_model=List[CultureRead])
async def read_cultures_by_utilisateur_endpoint(
    session: Session = Depends(get_session),
    utilisateur_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL))
):
    if utilisateur_current.role == "Agriculteur" and utilisateur_current.id != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les permissions nécessaires pour voir les cultures de cet utilisateur"
        )
    
    cultures = read_cultures_by_utilisateur(session=session, utilisateur_id=utilisateur_id)

    if not cultures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Culture inexistante"
        )
    return cultures 

@router.get("/ferme/{ferme_id}", response_model=List[CultureRead])
async def read_cultures_by_ferme_endpoint(
    session: Session = Depends(get_session),
    ferme_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ALL))
):
    cultures = read_cultures_by_ferme(session=session, ferme_id=ferme_id)

    if not cultures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Culture inexistante"
        )
    
    if utilisateur_current.role == "Agriculteur" and all(culture.utilisateur_id != utilisateur_current.id for culture in cultures):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les permissions nécessaires pour voir les cultures de cette ferme"
        )
    
    return cultures


@router.put("/{culture_id}", response_model=CultureRead)
async def update_culture_endpoint(
    session: Session = Depends(get_session),
    culture_id: int = Path(...),
    culture_data: CultureUpdate = Body(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR))
):
    culture = read_culture(session=session, culture_id=culture_id)

    if not culture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Culture inexistante"
        )
    
    if culture.utilisateur_id != utilisateur_current.id and utilisateur_current.role == "Agriculteur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les permissions nécessaires pour modifier cette culture"
        )
    
    culture = update_culture(session=session, culture_id=culture_id, culture=culture_data)

    return culture


@router.delete("/{culture_id}", response_model=CultureRead)
async def delete_culture_endpoint(
    session: Session = Depends(get_session),
    culture_id: int = Path(...),
    utilisateur_current: Utilisateur = Depends(requires_role(*ROLES_ADMIN_AGRICULTEUR))
):
    culture = read_culture(session=session, culture_id=culture_id)
    if not culture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Culture inexistante"
        )
    
    if culture.utilisateur_id != utilisateur_current.id and utilisateur_current.role == "Agriculteur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les permissions nécessaires pour supprimer cette culture"
        )
    culture = delete_culture(session=session, culture_id=culture_id)

    return culture
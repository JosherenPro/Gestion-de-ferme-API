from fastapi import Query, HTTPException
from sqlmodel import select

from app.core.session import Session
from app.models.ferme import Ferme
from app.schemas.ferme import (
    FermeCreate,
    FermeUpdate
)

# creer une ferme
def create_ferme(
        *,
        session: Session,
        ferme: FermeCreate
):
    db_ferme = Ferme.model_validate(ferme)
    session.add(db_ferme)
    session.commit()
    session.refresh(db_ferme)
    return db_ferme

# recuperer des fermes
def read_fermes(
        *,
        session: Session,
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    fermes = session.exec(select(Ferme).offset(offset).limit(limit)).all()
    return fermes

# recuperer une ferme avec un id
def read_ferme(
        *,
        session: Session,
        ferme_id: int
):
    ferme = session.get(Ferme, ferme_id)
    if not ferme:
        None
    return ferme

def read_ferme_by_utilisateur(
        *,
        session: Session,
        utilisateur_id: int
):
    fermes = session.exec(select(Ferme).where(Ferme.utilisateur_id==utilisateur_id)).all()
    return fermes

# mettre a jour une ferme
def update_ferme(
        *,
        session: Session,
        ferme_id: int,
        ferme: FermeUpdate
):
    db_ferme = session.get(Ferme, ferme_id)
    if not ferme:
        None
    ferme_data = ferme.model_dump(exclude_unset=True)
    db_ferme.sqlmodel_update(ferme_data)
    session.add(db_ferme)
    session.commit()
    session.refresh(db_ferme)
    return db_ferme

# supprimer une ferme
def delete_ferme(
        *,
        session: Session,
        ferme_id: int
):
    ferme = session.get(Ferme, ferme_id)
    if not ferme:
        return None
    session.delete(ferme)
    session.commit()
    return ferme
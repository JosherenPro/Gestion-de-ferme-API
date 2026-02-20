from fastapi import Query
from sqlmodel import select, func

from app.core.session import Session
from app.core.security import hash_password, verify_password

from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate


def get_user_by_email(session: Session, email: str):
    script = select(Utilisateur).where(func.lower(Utilisateur.email) == email.lower())
    return session.exec(script).first()


# authentification
def authentificate_user(session: Session, email: str, password: str):
    utilisateur = get_user_by_email(session=session, email=email)
    if not utilisateur:
        return False
    if not verify_password(password, utilisateur.hashed_password):
        return False
    return utilisateur


# creer un utilisateur
def create_utilisateur(*, session: Session, utilisateur: UtilisateurCreate):
    password = utilisateur.password
    hashed_password = hash_password(password)
    db_utilisateur = Utilisateur(
        nom=utilisateur.nom,
        prenom=utilisateur.prenom,
        email=utilisateur.email,
        hashed_password=hashed_password,
        role=utilisateur.role,
    )
    session.add(db_utilisateur)
    session.commit()
    session.refresh(db_utilisateur)
    return db_utilisateur


# recuperer des utilsateurs
def read_utilisateurs(
    *, session: Session, offset: int = 0, limit: int = Query(default=100, le=100)
):
    utilisateurs = session.exec(select(Utilisateur).offset(offset).limit(limit)).all()
    return utilisateurs


# recuperer un utilisateur avec un id
def read_utilisateur(*, session: Session, utilisateur_id: int):
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        return None
    return utilisateur


# mettre a jour un utilisateur
def update_utilisateur(
    *, session: Session, utilisateur_id: int, utilisateur: UtilisateurUpdate
):
    db_utilisateur = session.get(Utilisateur, utilisateur_id)
    if not db_utilisateur:
        return None
    utilisateur_data = utilisateur.model_dump(exclude_unset=True)
    db_utilisateur.sqlmodel_update(utilisateur_data)
    session.add(db_utilisateur)
    session.commit()
    session.refresh(db_utilisateur)
    return db_utilisateur


# supprimer un utilisateur
def delete_utilisateur(*, session: Session, utilisateur_id: int):
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        return None
    session.delete(utilisateur)
    session.commit()
    return utilisateur

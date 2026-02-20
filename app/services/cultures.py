from sqlmodel import select
from app.core.session import Session
from app.models.culture import Culture
from app.schemas.culture import CultureCreate, CultureUpdate


def create_culture(*, session: Session, culture_data: CultureCreate):
    culture = Culture.model_validate(culture_data)
    session.add(culture)
    session.commit()
    session.refresh(culture)
    return culture


def read_cultures(*, session: Session, offset: int = 0, limit: int = 100):
    cultures = session.exec(select(Culture).offset(offset).limit(limit)).all()
    return cultures


def read_cultures_by_ferme(*, session: Session, ferme_id: int):
    script = select(Culture).where(Culture.ferme_id == ferme_id)
    cultures = session.exec(script).all()
    return cultures


def read_cultures_by_utilisateur(*, session: Session, utilisateur_id: int):
    script = select(Culture).where(Culture.utilisateur_id == utilisateur_id)
    cultures = session.exec(script).all()
    return cultures


def read_culture(*, session: Session, culture_id: int):
    return session.get(Culture, culture_id)


def update_culture(*, session: Session, culture_id: int, culture_data: CultureUpdate):
    db_culture = session.get(Culture, culture_id)
    if not db_culture:
        return None
    culture_data = culture_data.model_dump(exclude_unset=True)
    db_culture.sqlmodel_update(culture_data)
    session.add(db_culture)
    session.commit()
    session.refresh(db_culture)
    return db_culture


def delete_culture(*, session: Session, culture_id: int):
    culture = session.get(Culture, culture_id)
    if not culture:
        return None
    session.delete(culture)
    session.commit()
    return culture

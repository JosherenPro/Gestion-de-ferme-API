from sqlmodel import SQLModel
from app.models.ferme import FermeBase


class FermeCreate(FermeBase):
    pass

class FermeRead(FermeBase):
    id: int


class FermeUpdate(SQLModel):
    nom: str | None = None
    localisation: str | None = None
    perimetre: str = None
    aire: str = None
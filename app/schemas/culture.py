from sqlmodel import SQLModel
from app.models.culture import CultureBase


class CultureCreate(CultureBase):
    pass

class CultureRead(CultureBase):
    id: int


class CultureUpdate(SQLModel):
    type: str | None = None
    perimetre: str | None = None
    aire: str | None = None
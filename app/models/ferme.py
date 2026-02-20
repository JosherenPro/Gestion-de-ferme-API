from sqlmodel import SQLModel, Field, Relationship

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.utilisateur import Utilisateur
    from app.models.culture import Culture


class FermeBase(SQLModel):
    nom: str = Field(index=True)
    localisation: str = Field(index=True)
    perimetre: float | None = Field(default=None)
    aire: float = Field(index=True)

    utilisateur_id: int | None = Field(default=None, foreign_key="utilisateur.id")


class Ferme(FermeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    utilisateur: "Utilisateur" = Relationship(back_populates="fermes")
    cultures: List["Culture"] = Relationship(back_populates="ferme")

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.ferme import Ferme
    from app.models.utilisateur import Utilisateur



class CultureBase(SQLModel):
    type: str = Field(index=True)
    perimetre: str = Field(index=True)
    aire: float = Field(index=True)
    date_culture: datetime = Field(
        default_factory= lambda: datetime.now(timezone.utc)
    )

    ferme_id: int | None = Field(default=None, foreign_key="ferme.id")
    utilisateur_id: int | None = Field(default=None, foreign_key="utilisateur.id")


class Culture(CultureBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    ferme: Ferme | None = Relationship(back_populates="cultures")
    utilisateur: Utilisateur | None = Relationship(back_populates="cultures")
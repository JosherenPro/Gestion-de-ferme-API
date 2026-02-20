from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ferme import Ferme
    from app.models.culture import Culture



class RoleEnum(str, Enum):
    admin = "Admin"
    agriculteur = "Agriculteur"
    technicien = "Technicien"


class UtilisateurBase(SQLModel):
    nom: str = Field(index=True)
    prenom: str = Field(index=True)
    email: str = Field(index=True)
    is_active: bool = Field(default=True)
    role: RoleEnum = Field(default=RoleEnum.agriculteur)


class Utilisateur(UtilisateurBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    fermes: List["Ferme"] = Relationship(back_populates="utilisateur")
    cultures: List["Culture"] = Relationship(back_populates="utilisateur")
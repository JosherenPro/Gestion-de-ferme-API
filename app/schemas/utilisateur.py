from sqlmodel import SQLModel
from app.models.utilisateur import UtilisateurBase


class UtilisateurCreate(UtilisateurBase):
    password: str


class UtilisateurRead(UtilisateurBase):
    id: int


class UtilisateurUpdate(SQLModel):
    nom: str | None = None
    prenom: str | None = None
    email: str | None = None
    password: str = None


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: str | None = None
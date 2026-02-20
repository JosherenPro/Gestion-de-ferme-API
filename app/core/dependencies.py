from app.core.security import oauth2_scheme
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.session import get_session, Session
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import TokenData, UtilisateurRead
from app.services.utilisateurs import get_user_by_email
from fastapi import Depends, HTTPException, status
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider votre connexion",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception

    utilisateur = get_user_by_email(session, email=token_data.email)

    if utilisateur is None:
        raise credentials_exception

    return utilisateur


async def get_current_active_user(
    current_utilisateur: Annotated[Utilisateur, Depends(get_current_user)]
):
    if not current_utilisateur.is_active:
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    return current_utilisateur


def requires_role(*roles: str):
    def role_checker(
        current_utilisateur: Annotated[Utilisateur, Depends(get_current_active_user)]
    ):
        if current_utilisateur.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas les permissions nécessaires pour accéder à cette ressource"
            )
        return current_utilisateur
    return role_checker
from fastapi import FastAPI
from contextlib import asynccontextmanager

import app.models
from app.routers import cultures, utilisateurs, fermes
from app.core.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Gestion de Ferme", lifespan=lifespan)

app.include_router(utilisateurs.router)
app.include_router(fermes.router)
app.include_router(cultures.router)

import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")


SECRET_KEY = os.getenv("SECRET_KEY", "openssl rand -hex 32")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

DEBUG = os.getenv("DEBUG", "True") in ("True", "true", True)

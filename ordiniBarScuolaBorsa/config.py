import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///data.db"   # default attuale
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
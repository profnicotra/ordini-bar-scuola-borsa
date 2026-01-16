import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///data.db"   # default attuale
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
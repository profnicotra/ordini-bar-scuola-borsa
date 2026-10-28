import os
import secrets

SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
DOMINIO_PROFESSORI = os.environ.get("DOMINIO_PROFESSORI", "scuola-borsa.it").lower()
ADMIN_EMAILS = {
    email.strip().lower()
    for email in os.environ.get("ADMIN_EMAILS", "").split(",")
    if email.strip()
}
REQUIRE_OPERATOR_LOGIN = os.environ.get("REQUIRE_OPERATOR_LOGIN", "true").strip().lower() != "false"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    "sqlite:///data.db"   # default attuale
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)


def sqlite_uri(filename: str = "banco_de_dados.db") -> str:
    return f"sqlite:///{INSTANCE_DIR / filename}"


def normalize_database_url(url: str | None) -> str | None:
    """
    Normaliza a URL vinda do ambiente para algo que o SQLAlchemy + psycopg2 aceite:
    - transforma 'postgres://' ou 'postgresql://' em 'postgresql+psycopg2://'
    - garante sslmode=require (útil para Supabase)
    """
    if not url:
        return None

    # prefixo psycopg2
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # forçar sslmode=require se não existir
    parts = urlsplit(url)
    q = dict(parse_qsl(parts.query))
    if "sslmode" not in q:
        q["sslmode"] = "require"
    new_query = urlencode(q)
    parts = parts._replace(query=new_query)
    return urlunsplit(parts)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    _env_url = os.environ.get("DEV_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = normalize_database_url(_env_url) or sqlite_uri()


class ProductionConfig(Config):
    DEBUG = False
    _env_url = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = normalize_database_url(_env_url) or sqlite_uri()
import os
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

# ... seu basedir e classes anteriores ...

def _normalize_database_url(url: str | None) -> str | None:
    if not url:
        return None
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    parts = urlsplit(url)
    q = dict(parse_qsl(parts.query))
    if "sslmode" not in q:
        q["sslmode"] = "require"
    new_query = urlencode(q)
    parts = parts._replace(query=new_query)
    return urlunsplit(parts)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(os.environ.get("DEV_DATABASE_URL")) \
        or 'sqlite:///' + os.path.join(basedir, 'instance', 'banco_de_dados.db')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(os.environ.get("DATABASE_URL")) \
        or 'sqlite:///' + os.path.join(basedir, 'instance', 'banco_de_dados.db')
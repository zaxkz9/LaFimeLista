import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
# Falls back to a local SQLite file when DATABASE_URL isn't set (e.g. Docker/Postgres
# isn't running yet). Set DATABASE_URL in .env to switch to Postgres — no code change needed.
default_dev_db_uri = "sqlite:///" + os.path.join(basedir, "instance", "dev.db")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", default_dev_db_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DUE_SOON_WINDOW = timedelta(days=3)


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")
    WTF_CSRF_ENABLED = False


config_by_name = {
    "development": DevConfig,
    "production": ProdConfig,
    "testing": TestConfig,
}

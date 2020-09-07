import os


def get_env_variable(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        message = f"expected environment variable {name} not set."
        raise Exception(message)


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

    POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
    POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_DB_NAME = get_env_variable("POSTGRES_DB_NAME")
    POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    USER_JWT_SECRET_KEY = get_env_variable("USER_JWT_SECRET_KEY")
    CORS_ORIGINS = get_env_variable("CORS_ORIGINS")
    CORS_METHODS = get_env_variable("CORS_METHODS")
    CORS_HEADERS = get_env_variable("CORS_HEADERS")


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
    POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_DB_NAME = get_env_variable("POSTGRES_DB_NAME")
    POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    USER_JWT_SECRET_KEY = get_env_variable("USER_JWT_SECRET_KEY")
    CORS_ORIGINS = get_env_variable("CORS_ORIGINS")
    CORS_METHODS = get_env_variable("CORS_METHODS")
    CORS_HEADERS = get_env_variable("CORS_HEADERS")


class ProductionConfig(Config):
    POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
    POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_DB_NAME = get_env_variable("POSTGRES_DB_NAME")
    POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    USER_JWT_SECRET_KEY = get_env_variable("USER_JWT_SECRET_KEY")
    CORS_ORIGINS = get_env_variable("CORS_ORIGINS")
    CORS_METHODS = get_env_variable("CORS_METHODS")
    CORS_HEADERS = get_env_variable("CORS_HEADERS")


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestConfig,
    prod=ProductionConfig
)

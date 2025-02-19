import os
import secrets
from datetime import timedelta
from twitter.settings import ROOT_PATH


class Config(object):
    # Flask
    SECRET_KEY = secrets.token_hex(32)
    # Flask Jwt Extended
    JWT_SECRET_KEY = secrets.token_hex(64)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # !(override them in production)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # !(override them in production)
    # Flask Uploads
    UPLOADED_PHOTOS_DEST = "uploads/images"
    UPLOADED_FILES_DEST = "uploads/images"
    UPLOADED_FILES_URL = "http://localhost:5001/photos"
    UPLOADED_FILES_ALLOW = ["png", "jpg", "jpeg", "gif", "mp4", "mkv"]
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.curdir), "/static")
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "mp4", "mkv"]
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    # better to load from environment like this : export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_COOKIE_SECURE = True
    DEBUG = False


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

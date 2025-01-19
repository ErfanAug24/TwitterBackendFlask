import secrets
import os
from flask import current_app


class Config(object):
    SECRET_KEY = secrets.token_hex(32)
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.curdir), "/Statics")
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

    # better to load from environment like this : export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass

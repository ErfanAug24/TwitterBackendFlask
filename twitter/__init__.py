import sys
from typing import List
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from .sqlalchemy_conf import db, register_cli
from .jwt_conf import jwt
from .bcrypt_conf import bcrypt

# import flask_swagger_ui too
from flask_socketio import SocketIO

# from redis import Redis
import os
from .settings import ROOT_PATH

# Extensions Initialization


migrate = Migrate()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
socketio = SocketIO()
parent = Blueprint("parent", __name__, url_prefix="/api")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(app.instance_path, 'twitter.db')}"
    )

    register_instance_path(app)
    mode = os.getenv("TWITTER_MODE", "development")
    if test_config is None:
        app.config.from_object("config.Config")
        if mode == "production":
            app.config.from_object("config.ProductionConfig")
        else:
            app.config.from_object("config.DevelopmentConfig")
        try:
            app.config.from_envvar("TWITTER_SETTINGS")
        except RuntimeError:
            pass
    else:
        app.config.from_mapping(test_config)

    # Validate required configurations
    if not app.config.get("SECRET_KEY"):
        from instance.config import Config

        app.config["SECRET_KEY"] = Config.SECRET_KEY

    jwt.init_app(app)
    db.init_app(app)
    register_cli(app)
    migrate.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    socketio.init_app(app)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # register blueprints here.
    from .Routes import Auth, TweetRoute

    register_blueprints([Auth.bp, TweetRoute.bp])
    app.register_blueprint(parent)
    return app


def register_instance_path(app: Flask):
    sys.path.append(app.instance_path)


def register_blueprints(blueprints: List[Blueprint]):
    for blueprint in blueprints:
        parent.register_blueprint(blueprint)

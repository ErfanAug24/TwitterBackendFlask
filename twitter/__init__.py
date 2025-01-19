from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# import flask_swagger_ui too
from flask_socketio import SocketIO

# from redis import Redis
import os


class Base(DeclarativeBase):
    pass


# Extensions Initialization


jwt = JWTManager()
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
cors = CORS()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
socketio = SocketIO()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(app.instance_path, 'twitter.db')}"
    )
    mode = os.getenv("TWITTER_MODE", "development")
    if test_config is None:
        app.config.from_object("config.Config")
        if mode == "production":
            app.config.from_object("config.Production")
        else:
            app.config.from_object("config.Development")
        try:
            app.config.from_envvar("TWITTER_SETTINGS")
        except RuntimeError:
            pass
    else:
        app.config.from_mapping(test_config)

    # Validate required configurations
    if not app.config.get("SECRET_KEY"):
        from config import Config

        app.config["SECRET_KEY"] = Config.SECRET_KEY

    jwt.init_app(app)
    db.init_app(app)
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

    return app

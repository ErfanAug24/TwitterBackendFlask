from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# import flask_swagger_ui too
from flask_socketio import SocketIO

# from redis import Redis
import os

# Extensions Initialization

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
socketio = SocketIO()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_object("config.Config")
    else:
        app.config.from_mapping(test_config)

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    socketio.init_app(app)
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    return app

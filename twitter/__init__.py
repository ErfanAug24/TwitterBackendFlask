import sys
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from typing import List

from .Config import sqlalchemy_conf, jwt_conf, bcrypt_conf
from .Config.sqlalchemy_conf import db
from .Config import upload_conf

# import flask_swagger_ui too
from flask_socketio import SocketIO

# from redis import Redis
import os


# Extensions Initialization

mamad = Blueprint("askhar", __name__, url_prefix="/api")
migrate = Migrate(db=db)
cors = CORS()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
socketio = SocketIO()


def create_app(test_config=None, testing: bool = False):
    """
    :param test_config:dict ==> mapping
    :param testing:bool
    :return: app:Flask
    """
    # app configuration
    app = Flask(__name__, instance_relative_config=True)
    # twitter.db path configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(app.instance_path, 'twitter.db')}"
    )
    # adding instance/ folder path to sys.path list
    sys.path.append(app.instance_path)
    app.config.from_object("config.Config")
    # facility to change application config
    mode = os.getenv("TWITTER_MODE", "development")
    if test_config is None:

        if mode == "production":
            app.config.from_object("config.ProductionConfig")
        else:
            app.config.from_object("config.DevelopmentConfig")
        try:
            # loading application config from different files via path/to/file
            app.config.from_envvar("TWITTER_SETTINGS")
        except RuntimeError:
            pass
    if test_config:
        app.config.from_mapping(test_config)
    if testing:
        app.config.from_object("config.TestingConfig")

    # validate required configurations
    if not app.config.get("SECRET_KEY"):
        from instance.config import Config

        app.config["SECRET_KEY"] = Config.SECRET_KEY

    # passing application through libraries
    sqlalchemy_conf.init_app(app)
    jwt_conf.init_app(app)
    bcrypt_conf.init_app(app)
    sqlalchemy_conf.register_cli(app)
    migrate.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    socketio.init_app(app)
    upload_conf.init_app(app)
    try:
        # creating instance folder for development purpose
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # register blueprints here.
    from .Routes import Auth, TweetRoute, UserRoute

    register_parent_blueprints([Auth.bp, TweetRoute.bp, UserRoute.bp], app)

    @app.route("/index")
    def index():
        return "this is index"

    return app


def register_parent_blueprints(blueprints: List[Blueprint], app: Flask):
    for bp in blueprints:
        if bp.name not in app.blueprints:
            app.register_blueprint(bp)

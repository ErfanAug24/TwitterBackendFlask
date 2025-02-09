from flask_jwt_extended import JWTManager
from ..Services.TokenService import token_jwt_bridge
from ..Services.UserService import user_jwt_bridge


jwt = JWTManager()


def init_app(app):
    jwt.init_app(app)


# bridge registration
user_jwt_bridge(jwt)
token_jwt_bridge(jwt)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

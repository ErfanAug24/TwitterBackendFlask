from flask_jwt_extended import JWTManager
from .Services.UserService import get_user_by_username, get_user_by_id

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return get_user_by_id(identity)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

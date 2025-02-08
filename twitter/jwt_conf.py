from flask_jwt_extended import JWTManager
from .Services.UserService import get_user_by_id
from .Services.TokenService import get_token_by_jti

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return get_user_by_id(identity)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = get_token_by_jti(jti)
    return token is not None

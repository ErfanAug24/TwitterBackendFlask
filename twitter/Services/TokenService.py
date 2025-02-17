from typing import Optional
from datetime import datetime
from ..Models import Token

# from ..Config.sqlalchemy_conf import db
from ..Utils.Db_utils import ModelQueries


def token_queries():
    return ModelQueries(Token)


def revoke_token(
    jti: str,
    token: str,
    ttype: str,
    user_id: int,
    expiration: datetime,
    revoked_at: datetime,
    reason: str,
):
    token = Token(jti, token, ttype, user_id, expiration, revoked_at, reason)
    return token


def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    query = token_queries()
    jti = jwt_payload["jti"]
    token = query.get_object_by_value(jti=jti).first()
    return token is not None


def token_jwt_bridge(jwt):
    jwt.token_in_blocklist_loader(check_if_token_revoked)

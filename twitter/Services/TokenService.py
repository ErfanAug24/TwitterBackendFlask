from ..Models import Token
from ..Utils.Db_utils import ModelQueries


def token_queries():
    return ModelQueries(Token)


def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    query = token_queries()
    jti = jwt_payload["jti"]
    token = query.get_object_by_value(jti=jti).first()
    return token is not None


def token_jwt_bridge(jwt):
    jwt.token_in_blocklist_loader(check_if_token_revoked)

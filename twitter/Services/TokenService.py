from typing import Optional
from datetime import datetime
from ..Models import Token
from ..Config.sqlalchemy_conf import db


def get_token_by_jti(jti: str):
    return db.session.query(Token.id).filter_by(jti=jti).scalar()


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


def add_token(token: Token):
    db.session.add(token)


def save_changes():
    db.session.commit()


def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    # token = token_db_api.get_by_object("jti", jti)
    token = db.session.query(Token).filter_by(jti=jti).first()
    return token is not None


def token_jwt_bridge(jwt):
    jwt.token_in_blocklist_loader(check_if_token_revoked)

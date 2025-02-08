from typing import Optional
from datetime import datetime
from ..Models import Token
from ..sqlalchemy_conf import db


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

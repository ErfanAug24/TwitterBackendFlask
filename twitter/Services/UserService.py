from typing import Optional
from ..sqlalchemy_conf import db
from ..Models import User
from ..Schemas.UserSchema import UserSchema
from ..bcrypt_conf import bcrypt

user_schema = UserSchema(partial=True, session=db.session)


def get_user_by_id(uid: int):
    return User.query.get_or_404(uid, "Not Found")


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()


def set_hash_password(user: User, password: str):
    user.password_hash = bcrypt.generate_password_hash(password)
    return user


def get_user_by_email(email: str):
    return User.query.filter_by(email=email).first()


def is_user_verified(uid: int):
    return get_user_by_id(uid).is_verified


def get_user_tweets(uid: int):
    return get_user_by_id(uid).tweets


def get_user_followers(uid: int):
    return get_user_by_id(uid).followers


def get_user_followings(uid: int):
    return get_user_by_id(uid).followings


def get_user_comments(uid: int):
    return get_user_by_id(uid).comments


def get_user_replies(uid: int):
    return get_user_by_id(uid).replies


def get_user_reports_received(uid: int):
    return get_user_by_id(uid).reports_received


def get_user_reports_made(uid: int):
    return get_user_by_id(uid).reports_made


def get_user_restrictions(uid: int):
    return get_user_by_id(uid).restrictions


def get_user_likes(uid: int):
    return get_user_by_id(uid).likes


def create_basic_user(fullname: str, username: str, email: str, password: str):
    user = User(
        fullname=fullname,
        username=username,
        email=email,
        password_hash=bcrypt.generate_password_hash(password),
        is_verified=False,
    )
    return user


def check_password(email: str, password: str, username: Optional[str] = None):
    user: Optional[User] = None
    if username:
        user = get_user_by_username(username)
    else:
        user = get_user_by_email(email)
    if bcrypt.check_password_hash(user.password_hash, password):
        return user


def add_user(user: User):
    db.session.add(user)


def commit_changes():
    db.session.commit()


def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return get_user_by_id(identity)

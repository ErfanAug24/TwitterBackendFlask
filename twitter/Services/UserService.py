from typing import Optional
from ..Models import User
from ..Schemas.UserSchema import UserSchema
from ..Config.bcrypt_conf import bcrypt
from ..Utils.Db_utils import ModelQueries
from ..Config.sqlalchemy_conf import db


def user_queries():
    return ModelQueries(User)


user_schema = UserSchema(partial=True, session=db.session)


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
    user_db_api = user_queries()
    user: Optional[User] = None
    if username:
        user = user_db_api.get_by_object("username", username).first()
    else:
        user = user_db_api.get_by_object("email", email).first()
    if bcrypt.check_password_hash(user.password_hash, password):
        return user


def user_lookup_callback(_jwt_header, jwt_data):
    user_db_api = user_queries()
    identity = jwt_data["sub"]
    return user_db_api.get_by_object("id", identity).first()


def user_jwt_bridge(jwt):
    jwt.user_lookup_loader(user_lookup_callback)

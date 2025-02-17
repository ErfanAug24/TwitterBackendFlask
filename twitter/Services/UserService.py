import os
from werkzeug.utils import secure_filename
from ..Config.upload_conf import photos
from ..Models import User
from ..Schemas.UserSchema import UserSchema
from ..Config.bcrypt_conf import bcrypt
from ..Utils.Db_utils import ModelQueries
from ..Config.sqlalchemy_conf import db


def user_queries():
    return ModelQueries(User)


user_schema = UserSchema(partial=True, session=db.session)


def check_password(pass_hash: str, passwd: str):
    return bcrypt.check_password_hash(pass_hash, passwd)


def generate_passwd_hash(passwd: str):
    return bcrypt.generate_password_hash(passwd)


def user_lookup_callback(_jwt_header, jwt_data):
    user_db_api = user_queries()
    identity = jwt_data["sub"]
    return user_db_api.get_object_by_value(id=identity).first()


def user_jwt_bridge(jwt):
    jwt.user_lookup_loader(user_lookup_callback)


def upload(file, dest):
    if file.filename == "":
        return None
    filename = secure_filename(file.filename)
    filepath = os.path.join(dest, filename)
    file.save(filepath)
    return filepath


def retrieve(filename):
    return str(photos.url(filename))

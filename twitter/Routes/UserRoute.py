from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user
from ..Utils.Auth import csrf_token_required
from ..Utils.Validators import schema_validator
from ..Services.UserService import (
    upload,
    user_queries,
    user_schema,
    generate_passwd_hash,
    check_password,
)
from ..Schemas.UserSchema import UserSchema
from flask import current_app
from datetime import datetime

bp = Blueprint("user", __name__, url_prefix="/user")
GET = ["GET"]
POST = ["POST"]
GETandPOST = ["GET", "POST"]


@bp.route("/upload", methods=POST)
@jwt_required(fresh=True)
@csrf_token_required
def upload_image():
    if "photo" not in request.files:
        return jsonify({"msg": "No file uploaded!"}), 400
    file = request.files["photo"]
    filepath = upload(file, current_app.config["UPLOADED_PHOTOS_DEST"])
    if filepath is None:
        return jsonify({"msg": "No selected file!"}), 400

    if file.filename == "":
        return jsonify({"msg": "No selected file!"}), 400
    query = user_queries()
    query.update_obj(
        current_user, profile_picture_url=filepath, update_date=datetime.now()
    )
    query.save_changes()

    return jsonify({"msg": "File uploaded!", "filename": file.filename}), 200


@bp.route("/profile/password", methods=POST)
@jwt_required(fresh=True)
@csrf_token_required
@schema_validator(UserSchema)
def update_password(data):
    query = user_queries()

    # Ensure passwords are sent as plain text and hashed inside the function

    if data.password_hash == data.old_password_hash:
        return (
            jsonify(
                {"msg": "You cannot use your current password as your new password!"}
            ),
            400,
        )

    if not check_password(current_user.password_hash, data.old_password_hash):
        return (
            jsonify({"msg": "Access denied!"}),
            403,
        )
    if current_user.old_password_hash is not None and check_password(
        current_user.old_password_hash, data.password_hash
    ):
        return (
            jsonify({"msg": "You used this password before, please create a new one."}),
            400,
        )

    query.update_obj(
        current_user,
        old_password_hash=current_user.password_hash,  # Store the previous hash
        password_hash=generate_passwd_hash(data.password_hash),
        update_date=datetime.now(),
    )
    query.save_changes()

    return jsonify({"msg": "Your password was successfully changed!"}), 201


@bp.route("/profile", methods=POST)
@jwt_required(fresh=True)
@csrf_token_required
@schema_validator(UserSchema)
def update_profile(data):
    query = user_queries()
    if not query.check_unique("username", data.username):
        return jsonify({"msg": "username should be unique"}), 400
    if not query.check_unique("email", data.email):
        return jsonify({"msg": "email should be unique"}), 400
    query.update_obj(
        current_user,
        username=data.username,
        email=data.email,
        phone=data.password,
        birthdate=data.birthdate,
    )
    query.save_changes()
    return user_schema.dump(current_user), 201

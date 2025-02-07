import secrets

from flask import Blueprint, request, jsonify

# from flask.views import MethodView
from ..Services.UserService import (
    create_basic_user,
    add_user,
    commit_changes,
    user_schema,
    check_password,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    jwt_required,
    unset_jwt_cookies,
)

bp = Blueprint("auth", __name__)
GET = ["GET"]
POST = ["POST"]
GETandPOST = ["GET", "POST"]


@bp.route("/register", methods=POST)
def register():
    data = request.get_json(force=True)
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = create_basic_user(
        fullname=data["fullname"],
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    add_user(user)
    commit_changes()
    return user_schema.dump(data), 201


@bp.route("/login", methods=POST)
def login():
    data = request.get_json(force=True)
    errors = user_schema.validate(data)
    user = check_password(data["email"], data["password"], request.json.get("username"))
    if errors:
        return jsonify(errors), 400
    if user:
        access_token = create_access_token(str(user.id))
        double_submit_token = secrets.token_hex(32)
        refresh_token = create_refresh_token(str(user.id))
        response = jsonify(
            {
                "Auth": {
                    "status": "successful",
                    "tokens": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "double_submit_token": double_submit_token,
                    },
                }
            }
        )
        set_access_cookies(response, access_token)
        return response, 201

    response = jsonify(
        {"Auth": {"status": "failure", "reason": "entries valued unacceptable"}}
    )

    return response, 403


@bp.route("/logout", methods=POST)
@jwt_required()
def logout():
    response = jsonify({"msg": "logged out successfully!"})
    unset_jwt_cookies(response)
    return response, 200


@bp.route("/protected", methods=GET)
@jwt_required(locations=["headers"])
def protected():
    client_double_submit_token = request.headers.get("X-CSRF-Token")
    if not client_double_submit_token:
        return jsonify({"msg": "Missing CSRF token"}), 403
    return jsonify({"msg": "this is protected route"})

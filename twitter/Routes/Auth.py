from flask import Blueprint, request, jsonify
from ..Utils.Auth import csrf_token_required
from datetime import datetime, timedelta, timezone
from ..Services import TokenService

from ..Services.UserService import (
    create_basic_user,
    user_schema,
    check_password,
    user_queries,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    jwt_required,
    unset_jwt_cookies,
    get_csrf_token,
    get_jwt,
    get_jwt_identity,
    current_user,
)


bp = Blueprint("auth", __name__)
GET = ["GET"]
POST = ["POST"]
GETandPOST = ["GET", "POST"]


@bp.route("/register", methods=POST)
def register():
    query = user_queries()
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
    query.get_db().add(user)
    query.get_db().commit()
    return user_schema.dump(data), 201


@bp.route("/test", methods=GET)
def test():
    query = user_queries()
    return user_schema.dump(query.get_by_object("username", "erfan").first())


@bp.route("/login", methods=POST)
def login():
    data = request.get_json(force=True)
    errors = user_schema.validate(data)
    user = check_password(data["email"], data["password"], request.json.get("username"))
    if errors:
        return jsonify(errors), 400
    if user:
        access_token = create_access_token(str(user.id), fresh=timedelta(minutes=15))
        csrf_token = get_csrf_token(access_token)
        refresh_token = create_refresh_token(str(user.id))
        response = jsonify(
            {
                "Auth": {
                    "status": "successful",
                    "tokens": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "csrf_token": csrf_token,
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


@bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    query = TokenService.token_queries()
    response = jsonify({"msg": "JWT Revoked!"})
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    exp_timestamp = token["exp"]
    _token = query.get_by_object("jti", jti).first()
    now = datetime.now(timezone.utc)
    TokenService.revoke_token(
        jti, _token, ttype, current_user["id"], exp_timestamp, now, "logout"
    )
    unset_jwt_cookies(response)
    return response, 200


@bp.route("/refresh", methods=POST)
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity(), fresh=False)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@bp.route("/protected", methods=GET)
@jwt_required(locations=["headers"], fresh=True)
@csrf_token_required
def protected():
    return jsonify(message="Access granted with valid CSRF token!"), 200

from flask import Blueprint, request, jsonify
from ..Utils.Auth import csrf_token_required
from datetime import datetime, timedelta, timezone
from ..Services import TokenService

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
    response = jsonify({"msg": "JWT Revoked!"})
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    exp_timestamp = token["exp"]
    _token = TokenService.get_token_by_jti(jti)
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
    # csrf_header = request.headers.get("X-CSRF-TOKEN")
    # csrf_token = get_csrf_token(request.cookies.get("access_token_cookie"))
    # if csrf_header != csrf_token:
    #     return jsonify({"msg": "CSRF token is missing or invalid"}), 403
    return jsonify(message="Access granted with valid CSRF token!"), 200

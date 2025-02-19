from flask import Blueprint, jsonify
from ..Utils.Auth import csrf_token_required
from datetime import datetime, timedelta, timezone
from ..Services.TokenService import token_queries
from ..Schemas.UserSchema import UserSchema
from ..Utils.Validators import schema_validator

from ..Services.UserService import (
    user_schema,
    check_password,
    generate_passwd_hash,
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
@schema_validator(UserSchema)
def register(data):
    query = user_queries()
    if not query.check_unique(username=data.username):
        return jsonify({"msg": "username is not unique."}), 409
    if not query.check_unique(email=data.email):
        return jsonify({"msg": "email is not unique."}), 409
    user = query.create_obj(
        fullname=data.fullname,
        username=data.username,
        email=data.email,
        password_hash=generate_passwd_hash(data.password_hash),
    )
    query.get_db().add(user)
    query.get_db().commit()
    return user_schema.dump(data), 201


@bp.route("/login", methods=POST)
@schema_validator(UserSchema)
def login(data):
    query = user_queries()
    user = query.get_object_by_value(email=data.email).first()
    print(user)
    if user and check_password(user.password_hash, data.password_hash):
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
        return response, 200

    response = jsonify(
        {"Auth": {"status": "failure", "reason": "entries valued unacceptable"}}
    )

    return response, 403


@bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    query = token_queries()
    response = jsonify({"msg": "JWT Revoked!"})
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    exp_timestamp = token["exp"]
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    _token = query.get_object_by_value(jti=jti).first()
    now = datetime.now(timezone.utc)
    revoked_token = query.create_obj(
        jti=jti,
        token=_token,
        ttype=ttype,
        user_id=current_user.id,
        expiration=exp_datetime,
        revoked_at=now,
        reason="logout",
    )
    query.add_obj(revoked_token)
    query.save_changes()
    unset_jwt_cookies(response)
    return response, 200


@bp.route("/refresh", methods=POST)
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token), 200


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

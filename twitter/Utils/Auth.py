from enum import Enum
from flask_jwt_extended import get_csrf_token
from flask import request, jsonify
import functools


class ReportOptions(Enum):
    SPAM = "SPAM"
    SEXUAL_CONTENT = "SEXUAL-CONTENT"
    HATE_SPEECH = "HATE-SPEECH"
    POLICY_VIOLATION = "POLICY-VIOLATION"
    OTHER = "OTHER"


def csrf_token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        csrf_header = request.headers.get("X-CSRF-TOKEN")
        csrf_token = get_csrf_token(request.cookies.get("access_token_cookie"))
        if csrf_header == csrf_token:
            return func(*args, **kwargs)
        return jsonify({"msg": "CSRF token is missing or invalid"}), 403

    return wrapper

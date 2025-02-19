from flask import jsonify

# Success responses
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_NO_CONTENT = 204

# Client error responses
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_CONFLICT = 409
HTTP_PAYLOAD_TOO_LARGE = 413
HTTP_TOO_MANY_REQUESTS = 429

# Server error responses
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_BAD_GATEWAY = 502
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_GATEWAY_TIMEOUT = 504


def bad_request(error="Bad Request"):
    return jsonify({"error": error}), HTTP_BAD_REQUEST


def unauthorized(error="Unauthorized"):
    return jsonify({"error": error}), HTTP_UNAUTHORIZED


def forbidden(error="Forbidden"):
    return jsonify({"error": error}), HTTP_FORBIDDEN


def not_found(error="Resource not found"):
    return jsonify({"error": error}), HTTP_NOT_FOUND


def method_not_allowed(error="Method Not Allowed"):
    return jsonify({"error": error}), HTTP_METHOD_NOT_ALLOWED


def conflict(error="Conflict detected"):
    return jsonify({"error": error}), HTTP_CONFLICT


def payload_too_large(error="Payload too large"):
    return jsonify({"error": error}), HTTP_PAYLOAD_TOO_LARGE


def too_many_requests(error="Too many requests"):
    return jsonify({"error": error}), HTTP_TOO_MANY_REQUESTS


# 5xx: Server Error Responses
def internal_server_error(error="Internal server error"):
    return jsonify({"error": error}), HTTP_INTERNAL_SERVER_ERROR


def bad_gateway(error="Bad Gateway"):
    return jsonify({"error": error}), HTTP_BAD_GATEWAY


def service_unavailable(error="Service Unavailable"):
    return jsonify({"error": error}), HTTP_SERVICE_UNAVAILABLE


def gateway_timeout(error="Gateway Timeout"):
    return jsonify({"error": error}), HTTP_GATEWAY_TIMEOUT


def no_content_response():
    return "", HTTP_NO_CONTENT

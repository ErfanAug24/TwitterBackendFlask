from flask import request, jsonify
from functools import wraps

from marshmallow import ValidationError
from twitter.Config.sqlalchemy_conf import db


def schema_validator(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json(force=True)
            try:
                object_schema = schema(session=db.session)
                validated_data = object_schema.load(data)
            except ValidationError as err:
                return jsonify({"errors": err.messages})

            return func(*args, **kwargs, data=validated_data)

        return wrapper

    return decorator

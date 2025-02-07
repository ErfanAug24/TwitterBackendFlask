import re

from marshmallow import ValidationError, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from . import Tweet


class TweetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tweet
        include_relationships = True
        load_instance = True
        include_fk = True

    @validates("title")
    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Too short title.")
        if re.match(r"^.{5,100}$", value) is None:
            raise ValidationError("Invalid title length.")
        if re.match(r"^[a-zA-Z0-9 .,!?-]+$") is None:
            raise ValidationError("Invalid title format.")

    @validates("body")
    def validate_body(self, value):
        if (
            re.match(r"^(?!\s)(?:(?!\s{2,})[\w\s.,!?@#&%()-]){10,5000}(?<!\s)$", value)
            is None
        ):
            raise ValidationError("Invalid body length or cosecutive spaces.")

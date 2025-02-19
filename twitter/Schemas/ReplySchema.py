from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import Reply
from marshmallow import validates, ValidationError
import re


class ReplySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reply
        include_relationships = True
        load_instance = True
        include_fk = True

    @validates("comment")
    def validate_body(self, value):
        if (
            re.match(r"^(?!\s)(?:(?!\s{2,})[\w\s.,!?@#&%()-]){10,5000}(?<!\s)$", value)
            is None
        ):
            raise ValidationError("Invalid comment")

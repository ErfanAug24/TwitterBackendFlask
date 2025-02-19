from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validates, ValidationError
from . import Comment
import re


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
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

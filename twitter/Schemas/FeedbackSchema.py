from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validates, ValidationError
from . import Feedback
import re


class FeedbackSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
        include_relationships = True
        load_instance = True
        include_fk = True

    @validates("content")
    def validate_content(self, value):
        pattern = r"^[a-zA-Z0-9.,!?()'\" -]{5,500}$"
        if not re.match(pattern, value):
            raise ValidationError("Invalid content.")

    @validates("category")
    def validate_category(self, value):
        pattern = "^[a-zA-Z ]{3,50}$"
        if not re.match(pattern, value):
            raise ValidationError("Invalid category.")

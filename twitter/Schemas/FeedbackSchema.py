from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import Feedback


class FeedbackSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback
        include_relationships = True
        load_instance = True
        include_fk = True

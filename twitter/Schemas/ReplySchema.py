from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import Reply


class ReplySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reply
        include_relationships = True
        load_instance = True
        include_fk = True

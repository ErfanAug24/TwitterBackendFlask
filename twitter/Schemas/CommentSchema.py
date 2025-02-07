from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import Comment


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True
        include_fk = True

from . import Like
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class LikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        include_relationships = True
        load_instance = True
        include_fk = True

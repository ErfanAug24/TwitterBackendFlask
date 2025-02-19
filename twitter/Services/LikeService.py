from ..Utils.Db_utils import ModelQueries
from ..Models.Reactions import Like
from ..Schemas.LikeSchema import LikeSchema
from ..Config.sqlalchemy_conf import db


def like_queries():
    return ModelQueries(Like)


like_schema = LikeSchema(session=db.session)

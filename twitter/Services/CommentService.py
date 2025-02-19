from ..Utils.Db_utils import ModelQueries
from ..Models.Reactions import Comment
from ..Schemas.CommentSchema import CommentSchema
from ..Config.sqlalchemy_conf import db


def comment_queries():
    return ModelQueries(Comment)


comment_schema = CommentSchema(session=db.session)

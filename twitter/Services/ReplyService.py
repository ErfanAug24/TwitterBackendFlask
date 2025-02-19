from ..Utils.Db_utils import ModelQueries
from ..Models.Reactions import Reply
from ..Schemas.ReplySchema import ReplySchema
from ..Config.sqlalchemy_conf import db


def reply_queries():
    return ModelQueries(Reply)


reply_schema = ReplySchema(session=db.session)

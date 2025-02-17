from ..Models import Tweet
from ..Utils.Db_utils import ModelQueries
from ..Schemas.TweetSchema import TweetSchema
from ..Config.sqlalchemy_conf import db


def tweet_queries():
    return ModelQueries(Tweet)


tweet_schema = TweetSchema(session=db.session)

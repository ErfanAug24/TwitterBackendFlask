from ..Utils.Db_utils import ModelQueries
from ..Models.Reactions import Follow


def follow_queries():
    return ModelQueries(Follow)

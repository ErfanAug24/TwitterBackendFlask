from ..Utils.Db_utils import ModelQueries
from ..Models import Feedback


def feedback_query():
    return ModelQueries(Feedback)

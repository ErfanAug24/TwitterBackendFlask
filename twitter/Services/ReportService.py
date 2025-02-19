from ..Utils.Db_utils import ModelQueries
from ..Models import Report
from ..Schemas.ReportSchema import ReportSchema
from ..Config.sqlalchemy_conf import db


def report_queries():
    return ModelQueries(Report)


report_schema = ReportSchema(session=db.session)

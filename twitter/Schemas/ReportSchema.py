from . import Report
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class ReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Report
        include_relationships = True
        load_instance = True
        include_fk = True

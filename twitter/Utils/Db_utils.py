from sqlalchemy.orm import class_mapper
from ..Config.sqlalchemy_conf import db


class VarCollector:
    def __init__(self, model):
        self._Model = model
        self._var_list = []
        self._var_dict = {}
        self.collect_model_vars()

    def get_var_list(self):
        return self._var_list

    def get_var_dict(self):
        return self._var_dict

    def collect_model_vars(self):
        self._var_list = [column.key for column in class_mapper(self._Model).columns]
        self._var_dict = {
            column: getattr(self._Model, column) for column in self._var_list
        }

    def is_var_exists(self, varname):
        return varname in self._var_list

    def get_var_value(self, varname):
        if self.is_var_exists(varname):
            return getattr(self._Model, varname)
        raise AttributeError(
            f"Field '{varname}' does not exist in {self._Model.__name__}"
        )

    def update_var(self, varname, value):
        if self.is_var_exists(varname):
            setattr(self._Model, varname, value)
            self._var_dict[varname] = value
            return self.get_var_value(varname)


class ModelQueries(VarCollector):
    def __init__(self, model):
        super().__init__(model)
        self._db_model = db.session.query(self._Model)
        self._db = db.session

    def save_changes(self):
        self._db.commit()

    def get_db_model(self):
        return self._db_model

    def get_db(self):
        return self._db

    def get_by_object(self, field, value):
        model_column = getattr(self._Model, field, None)
        if model_column is None:
            raise AttributeError(
                f"Field '{field}' does not exist in {self._Model.__name__}"
            )
        return self._db_model.filter(self.get_var_value(field) == value)

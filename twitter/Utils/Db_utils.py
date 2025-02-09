from sqlalchemy.orm import class_mapper
from ..Config.sqlalchemy_conf import db
from functools import wraps


def validate_model_fields(func):
    @wraps(func)
    def wrapper_validator(self, *args, **kwargs):
        for key in kwargs.keys():
            if not self.is_field_exists(key):
                raise AttributeError(
                    f"Field '{key}' does not exist in {self._Model.__name__}"
                )
        return func(self, *args, **kwargs)

    return wrapper_validator


class VarCollector:
    def __init__(self, model):
        self._Model = model
        self._var_list = []
        self._var_dict = {}
        self.collect_model_vars()

    def get_model(self):
        return self._Model

    def get_var_list(self):
        return self._var_list

    def get_var_dict(self):
        return self._var_dict

    def collect_model_vars(self):
        self._var_list = [column.key for column in class_mapper(self._Model).columns]
        self._var_dict = {
            column: getattr(self._Model, column) for column in self._var_list
        }

    def get_field_value(self, field):
        return getattr(self._Model, field, None)

    def is_field_exists(self, field):
        return hasattr(self._Model, field)

    @validate_model_fields
    def update_model_field_value(self, field, value):
        if self.get_field_value(field):
            setattr(self._Model, field, value)
            self._var_dict[field] = value


class ModelQueries(VarCollector):
    def __init__(self, model):
        super().__init__(model)
        self._db = db.session
        self._db_model = db.session.query(self._Model)

    def get_db(self):
        return self._db

    def get_db_model(self):
        return self._db_model

    def save_changes(self):
        self._db.commit()

    def add_obj(self, obj: db.Model):
        self._db.add(obj)

    @validate_model_fields
    def get_object_by_value(self, **kwargs):
        return self._db_model.filter_by(**kwargs)

    @validate_model_fields
    def create_obj(self, **kwargs):
        return self._Model(**kwargs)

    def delete_obj(self, obj: db.Model):
        self._db.delete(obj)

    @validate_model_fields
    def update_obj(self, obj: db.Model, **kwargs):
        for keyword, value in kwargs.items():
            self.update_model_field_value(keyword, value)
        return obj

    @validate_model_fields
    def check_unique(self, **kwargs):
        if self.get_object_by_value(**kwargs).first():
            return False
        return True

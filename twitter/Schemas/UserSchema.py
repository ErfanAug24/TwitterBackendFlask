from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validates, ValidationError, fields
from . import User
import re


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        include_fk = False
        load_instance = True
        exclude = ("password_hash",)

    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, attribute="password_hash")
    username = auto_field(required=False)
    fullname = auto_field(required=False)

    @validates("username")
    def validate_username(self, value):
        if not value:
            raise ValidationError("Username cannot be empty.")
        if len(value) > 30:
            raise ValidationError("Username cannot be longer than 30.")
        if len(value) < 3:
            raise ValidationError("Username must be longer than 3.")
        if value.startswith(
            ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+")
        ):
            raise ValidationError(
                "Username cannot start with any special operational character."
            )

    @validates("email")
    def validate_email(self, value):
        pattern = r"^(?!\.)[a-zA-Z0-9._%+-]+(?<!\.)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if len(value) < 10:
            raise ValidationError("Email must be longer than 10.")

        if re.match(pattern, value) is None:
            raise ValidationError("Not a valid email address.")

    @validates("fullname")
    def validate_fullname(self, value):
        pattern = r"^[a-zA-Z' -]+$"
        if re.match(pattern, value) is None:
            raise ValidationError("Fullname is invalid.")

    @validates("phone")
    def validate_phone(self, value):
        pattern = r"^\+[1-9]\d{1,14}$"
        if re.match(pattern, value) is None:
            raise ValidationError("Phone number is invalid.")

    @validates("password")
    def validate_password(self, value):
        pattern = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if re.match(pattern, value) is None:
            raise ValidationError("Password is invalid.")

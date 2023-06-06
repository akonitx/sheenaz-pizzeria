from menu.models import Customer
from django.contrib.auth.models import User
from django.forms import Form, CharField, EmailField, PasswordInput, TextInput
from menu.validators import (
    IntegrityValidator,
    NumberIntegrityValidator,
    UserExistanceValidator,
)


class UserCustomerRegistrationForm(Form):
    username = CharField(
        label="username",
        max_length=150,
        validators=[
            IntegrityValidator(
                message="User with entered username already exists",
                code="integrity",
                model=User,
                model_field="username",
            )
        ],
    )
    first_name = CharField(label="first name", max_length=150)
    last_name = CharField(label="last name", max_length=150)
    email = EmailField(label="email address", max_length=150)
    password = CharField(label="password", max_length=200, widget=PasswordInput())
    ua_phone_number = CharField(
        validators=[
            NumberIntegrityValidator(
                message="Entered phone number already exists",
                code="integrity",
                model=Customer,
                model_field="ua_phone_number",
            ),
        ],
        label="phone number +380",
        max_length=9,
        min_length=9,
    )


class Login(Form):
    username = CharField(
        label="username",
        max_length=150,
        validators=[
            UserExistanceValidator(
                message="Entered username does not exist. Try to register your entity.",
                code="integrity",
                model=User,
                model_field="username",
            )
        ],
    )
    password = CharField(label="password", max_length=150, widget=PasswordInput())


class UserUpdateProfile(Form):
    first_name = CharField(label="first name", max_length=150)
    last_name = CharField(label="last name", max_length=150)


class ChangeEmail(Form):
    email = EmailField(
        label="email address",
        max_length=150,
        widget=TextInput(attrs={"autocomplete": "new-password"}),
        validators=[
            IntegrityValidator(
                message="Entered email already exists",
                code="integrity",
                model=User,
                model_field="email",
            )
        ],
    )


class ChangePassword(Form):
    password = CharField(
        label="password",
        max_length=150,
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class ChangePhoneNumber(Form):
    ua_phone_number = CharField(
        label="phone number +380",
        max_length=9,
        min_length=9,
        widget=TextInput(attrs={"autocomplete": "new-password"}),
        validators=[
            NumberIntegrityValidator(
                message="Entered phone number already exists",
                code="integrity",
                model=Customer,
                model_field="ua_phone_number",
            ),
        ],
    )


class ChangeUsername(Form):
    username = CharField(
        widget=TextInput(attrs={"autocomplete": "new-password"}),
        label="username",
        max_length=150,
        validators=[
            IntegrityValidator(
                message="User with entered username already exists",
                code="integrity",
                model=User,
                model_field="username",
            )
        ],
    )

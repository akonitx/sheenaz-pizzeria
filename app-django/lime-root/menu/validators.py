from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from menu.models import Customer
from django.utils.deconstruct import deconstructible


class NumberValidator:
    """
    Checks number len
    """

    def phone_len(self, value):
        validationError = ValidationError(
            "Phone number must contain only 9 digits",
            code="valid ",
        )
        try:
            if not len(str(int(value))) == 9:
                raise validationError
        except ValueError:
            raise validationError


@deconstructible
class IntegrityValidator:
    def __init__(self, code, message, model, model_field):
        self.integrityError = ValidationError(
            message,
            code=code,
        )
        self.model = model
        self.model_field = model_field

    def __call__(self, value):
        filter = {f"{self.model_field}": value}

        if self.model.objects.filter(**filter).exists():
            raise self.integrityError


class NumberIntegrityValidator(IntegrityValidator, NumberValidator):
    def __call__(self, *args, **kwargs):
        self.phone_len(*args, **kwargs)
        super().__call__(*args, **kwargs)


class UserExistanceValidator(IntegrityValidator):
    def __call__(self, value):
        filter = {f"{self.model_field}": value}

        if not self.model.objects.filter(**filter).exists():
            raise self.integrityError

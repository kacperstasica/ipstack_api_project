from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import get_default_password_validators

from accounts.utils import flatten_list


def drf_based_password_validation(password, password_validators=None):
    """
    Custom validation needed in order to fix the bug with
    wrong error format in DRF Response.
    DRF Response error format returned string as a list of lists:
        '[["<error message>"]]'
    We overwrite Django validate_password and return
    flattened list of errors.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password)
        except DjangoValidationError as error:
            errors.append(error.messages)
    if errors:
        return flatten_list(errors)

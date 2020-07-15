from django.core.exceptions import ValidationError


def password_len_validation(value):
    if len(value) < 8:
        raise ValidationError("za krotkie haslo")
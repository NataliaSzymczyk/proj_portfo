from django.core.exceptions import ValidationError



def password_len_validation(value):
    if len(value) < 8:
        raise ValidationError("Hasło musi mieć minimum 8 znaków.")

def number_validator(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError("Hasło musi zawierać minimum jedną cyfrę.")

def lower_letter_validator(value):
    if not any(char.islower() for char in value):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 małą literę.")

def upper_letter_validator(value):
    if not any(char.isupper() for char in value):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 dużą literę.")

def special_character_validator(value):
    sp_characters = "[!#$%&'()*+,-./:;<=>?@'[\]^_`{|}\"~]"
    if not any(char in sp_characters for char in value):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 znak specjalny, czyli jeden z tych: " + sp_characters)


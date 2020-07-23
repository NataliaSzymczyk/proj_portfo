from django.core.exceptions import ValidationError



def password_len_validation(password1):
    if len(password1) < 8:
        raise ValidationError("Hasło musi mieć minimum 8 znaków.")

def number_validator(password1):
    if not any(char.isdigit() for char in password1):
        raise ValidationError("Hasło musi zawierać minimum jedną cyfrę.")

def lower_letter_validator(password1):
    if not any(char.islower() for char in password1):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 małą literę.")

def upper_letter_validator(password1):
    if not any(char.isupper() for char in password1):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 dużą literę.")

def special_character_validator(password1):
    sp_characters = "[!#$%&'()*+,-./:;<=>?@'[\]^_`{|}\"~]"
    if not any(char in sp_characters for char in password1):
        raise ValidationError("Hasło musi zawierać przynajmniej 1 znak specjalny, czyli jeden z tych: " + sp_characters)


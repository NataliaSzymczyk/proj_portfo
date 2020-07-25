from django.core.exceptions import ValidationError


class PasswordLenValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Hasło musi mieć minimum 8 znaków.")

    def get_help_text(self):
        return "Hasło musi mieć minimum 8 znaków."


class NumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Hasło musi zawierać minimum jedną cyfrę.")

    def get_help_text(self):
        return "Hasło musi zawierać minimum jedną cyfrę."


class LowLetterValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password1):
            raise ValidationError("Hasło musi zawierać przynajmniej 1 małą literę.")

    def get_help_text(self):
        return "Hasło musi zawierać przynajmniej 1 małą literę."


class UpperLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password1):
            raise ValidationError("Hasło musi zawierać przynajmniej 1 dużą literę.")

    def get_help_text(self):
        return "Hasło musi zawierać przynajmniej 1 dużą literę."


class SpecialCharacterValidator:
    def validate(self, password, user=None):
        sp_characters = "[!#$%&'()*+,-./:;<=>?@'[\]^_`{|}\"~]"
        if not any(char in sp_characters for char in password1):
            raise ValidationError(
                "Hasło musi zawierać przynajmniej 1 znak specjalny, czyli jeden z tych: " + sp_characters)

    def get_help_text(self):
        sp_characters = "[!#$%&'()*+,-./:;<=>?@'[\]^_`{|}\"~]"
        return "Hasło musi zawierać przynajmniej 1 znak specjalny, czyli jeden z tych" + sp_characters


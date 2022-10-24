import re

from django.core.exceptions import ValidationError
from django.core.validators import slug_re

PERSIAN_CHARACTER_REG = "^[پچجحخهعغفقثصضشسیبلاتنمآکگوئدذرزطظژؤإأءًٌٍَُِّ\s\n\r\t]+$"


class PersianValidations:

    @staticmethod
    def just_persian_chars(value):
        if re.search(PERSIAN_CHARACTER_REG, value):
            return True
        return False

    @staticmethod
    def phone_number(value):
        if not value or not re.search(r'^\d{11}$', value):
            return False
        return value.startswith('09')

    @staticmethod
    def code_meli(value):
        if not re.search(r'^\d{10}$', value):
            return False
        check = int(value[9])
        s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
        return (s < 2 and check == s) or (s >= 2 and check + s == 11)


class BadiValidators:

    @staticmethod
    def validate_persian(value):
        if not PersianValidations.just_persian_chars(value):
            raise ValidationError(
                f' مقدار '
                f'"{value}"'
                f' صحیح نمی باشد، لطفا فقط حروف فارسی استفاده کنید.'
            )

    @staticmethod
    def slug(value):
        if not re.search(r'^[-a-zA-Z0-9_۰۱۲۳۴۵۶۷۸۹پچجحخهعغفقثصضشسیبلاتنمآکگوئدذرزطظژؤإأء]+\Z', value):
            raise ValidationError('اسلاک آدرس وارد شده صحیح نمی باشد.')

    @staticmethod
    def username(value):
        is_valid = value and re.match("^[a-zA-Z0-9_]+$", value) and len(value) > 3 and not value.isdigit()
        return not not is_valid

    @staticmethod
    def is_mail(value):
        if not value or not re.search(r'[^@]+@[^@]+\.[^@]+', value):
            return False
        return value

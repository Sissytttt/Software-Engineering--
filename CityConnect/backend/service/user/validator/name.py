from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
from dao.models import Cient, BusinessOwner
from .common import validate_value

username_validators = [validate_slug]

def validate_name(name):
    validate_value(name, validators=username_validators)
    try:
        existing_u = Client.objects.get(auth__username=name)
        existing_b = BusinessOwner.objects.get(auth__username=name)
        if existing_u or existing_b:
            raise ValidationError(f"Name {name} has been used.")
    except Client.DoesNotExist and BusinessOwner.DoesNotExist:
        return 
from django.core.validators import validate_email as email_validator
from django.core.exceptions import ValidationError
from dao.models import Client, BusinessOwner
from .common import validate_value

email_validators = [email_validator]

def validate_email(email):
    validate_value(email, validators=email_validators) 
    try:
        existing_c = Client.objects.get(auth__email=email)
        existing_bo = BusinessOwner.objects.get(auth__email=email)
        if existing_c or existing_bo:
            raise ValidationError(f"Email {email} has been used.")
    except Client.DoesNotExist and BusinessOwner.DoesNotExist:
        return
from django.contrib.auth import authenticate as _authenticate
from django.db.models import Q
from dao.models import BusinessOwner, Client

from dao.models import User
from .validator import validate_email, validate_username, validate_password


def signup(email, name, password, phone, city, whether_bo):
    validate_email(email)
    validate_username(name)
    validate_password(password)
    
    if whether_bo == 1: #bo
      new_bo = BusinessOwner.objects.create(
        phone=phone
        city=city
      )
      new_bo.save()
      return new_bo
    else:
      new_cl = Client.objects.create(
        phone_number=phone
        city=city
      )
      new_cl.save()
      return new_cl
    
  
def authenticate(name, password):
    auth_user = _authenticate(username=name, password=password)
    if auth_user is None:
        return None
    try:
        existing_c = Client.objects.get(auth=auth_user)
        existing_bo = BusinessOwner.objects.get(auth=auth_user)
        if existing_c:
            return Client.objects.get(auth=auth_user)
        if existing_bo:
            return BusinessOwner.objects.get(auth=auth_user)
    except Client.DoesNotExist and BusinessOwner.DoesNotExist:
        return None
      

def get(phone):
  try:
    bo = BusienssOwner.objects.get(phone=phone)
  except BusinessOwner.DoesNotExist:
    try:
      cl = Client.objects.get(phone_number=phone)
    except Client.DoesNotExist:
      return None
    else:
      return cl
  else:
    return bo


def search_bo(keyword):
    return BusinessOwner.objects.filter(Q(username__icontains=keyword))
  
def search_cl(keyword):
    return Client.objects.filter(Q(username__icontains=keyword))

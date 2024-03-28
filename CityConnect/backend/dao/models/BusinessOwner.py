import mysql.connector
from django.db import models
from django.utils import timezone
from .models import Place

class BusinessOwner(models.Model):
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    

    def Search_Place(self, name, city=city):
        # change order by distance
        return Place.objects.filter(Q(name=name) & Q(city=city)).order_by("-creation_date")

    def Search_Event(self, name, city=city, Etype, NotFull=True):
        # change order by distance
        return Event.objects.filter(Q(name=name) & Q(city=city) & Q(event_type=Etype) & Q(Check_Full=full)).order_by("-creation_date")

    def Post_Event(self, name, start_time, end_time, description=None, max_ppl, event_type, Place):
        return Event.objects.create(
            name = name,
            business_owner = self,
            start_time = start_time,
            end_time = end_time,
            description = description,
            max_ppl = max_ppl, 
            current_ppl = 0,
            score = 5,
            avg_price = 0,
            event_type = event_type,
            place = Place,
        )
    
    def Delete_Event(self, event):
        if event.business_owner == self:
            event.delete()

    def Get_Phone(self):
        return self.phone

    def Get_City(self):
        return self.city

    def Set_Phone(self, phone):
        self.phone = phone
    
    def Set_City(self, city):
        self.city = city
import mysql.connector
from django.db import models
from django.utils import timezone

from .models import Place
from .models import Event

class Client(models.Model):

    phone_number = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    follows = models.ManyToManyField('self', related_name='followers', related_query_name='follower', to='dao.client')

    def Search_Place(self, name, city=city):
        # change order by distance
        return Place.objects.filter(Q(name=name) & Q(city=city)).order_by("-creation_date")
    
    def Search_Event(self, name, city, start_time, end_time, Etype, full):
        return Event.objects.filter(Q(name=name) & Q(start_time=start_time) & Q(end_time=end_time) & Q(Etype=Etype) & Q(Check_full=full)).order_by("-creation_date")
    
    def RSVP_Event(self, event):
        # update event attribute
        if event.check_full() == True and event.get_current_ppl() < event.get_max_ppl():
            event.update_current_ppl(event.get_current_ppl()+1)
        # update rsvp many to many table
        return Event.objects.filter(Q(current_ppl__in=self)).order_by("-creation_date") # return a list of events rsvp by the client
    
    def Cancel_Event(self, event):
        if self.events.filter(id=event.id).exists():
            event.update_current_ppl(event.get_current_ppl() - 1)
        return Event.objects.filter(Q(current_ppl__in=self)).order_by("-creation_date")
    
    def View_Map(self):
        return
    
    def Add_To_Map(self):
        return
    
    def Delete_From_Map(self):
        return
    
    def Post_Event_Review(self):
        return
    
    def Delete_Event_Review(self):
        return
    
    def Get_Followers(self):
        return self.followers.all()
    
    def Get_Follows(self):
        return self.follows.all()
    
    def Follow(self, followee):
        self.follows.add(followee)
        self.save()
    
    def Unfollow(self, followee):
        self.follows.remove(followee)
        self.save()
    

# Example usage:
# Initialize the Place object with your MySQL database credentials
place = Place(host='127.0.0.1', user='root', password='', database='software_engineering')

# Set the name of the place to fetch its details
# place.Set_Name("Eiffel Tower")

# Access the details
name = place.Get_Name(longitude='48.8583720000', latitude='2.2944810000')
print(name)  # Eiffel Tower

# longitude = place.Get_location_longitude("Eiffel Tower")
# print(longitude)

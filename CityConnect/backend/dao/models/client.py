import mysql.connector
from django.db import models
from django.utils import timezone

from .models import Place, Event, Event_Review, Save

class Client(models.Model):

    phone_number = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    follows = models.ManyToManyField('self', related_name='followers', related_query_name='follower')
    added_places = models.ManyToManyField(Place, related_name='added_by_clients', related_query_name='place')
    added_events = models.ManyToManyField(Event, related_name='events_added_by_clients', related_query_name='event')

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
        cities = self.added_places.values_list('city', flat=True).distinct()
        return list(cities)
    
    def Add_To_Map(self, place_id):
        try:
            place = Place.objects.get(id=place_id)
            self.added_places.add(place)
            self.save()
            return True
        except Place.DoesNotExist:
            return False
    
    def Delete_From_Map(self, place_id):
        try:
            place = Place.objects.get(id=place_id)
            self.added_places.remove(place)
            self.save()
            return True
        except Place.DoesNotExist:
            return False
    
    def Post_Event_Review(self, id, event, content, rating, price, creation_date):
        review = Event_Review.objects.create(id=id, event=event, client=self, content=content, rating=rating, price=price, creation_date=creation_date)
        return review
    
    def Delete_Event_Review(self, id):
        try:
            review = Event_Review.objects.get(id=id, client=self)
            review.delete()
            return True
        except Event_Review.DoesNotExist:
            return False
    
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

    def get_added_places(self):
        return self.added_places.all()
    
    def get_added_events(self):
        return self.added_places.all()
    
    def list_places(self):
        return Place.objects.filter(Q(name=self))
    
    def like(self, place):
        try:
            Save.objects.get(user=self, place=place)
        except Save.DoesNotExist:
            Save.objects.create(
                user = self,
                place = place
            )
    
    def unlike(self, place):
        try:
            save = Save.objects.get(user=self, place=place)
            save.delete()
        except Save.DoesNotExist:
            return
    

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

import mysql.connector
from django.db import models
from django.utils import timezone

class Client(models.Model):
    phone_number = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    follows = models.ManyToManyField(related_name='followers', related_query_name='follower', to='dao.client')

    def Search_Place(self):
        return
    
    def Search_Event(self):
        return
    
    def RSVP_Event(self):
        return
    
    def Cancel_Event(self):
        return
    
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
        return
    
    def Get_Follows(self):
        return
    
    def Follow(self):
        return
    
    def Unfollow(self):
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

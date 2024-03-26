import mysql.connector
from django.db import models
from django.utils import timezone

class Place(models.Model):
    # def __init__(self, host, user, password, database):
        # self.connection = mysql.connector.connect(
        #     host=host,
        #     user=user,
        #     password=password,
        #     database=database
        # )
        # self.name = None
        # self.longitude = None
        # self.latitude = None
        # self.city = None
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    city = models.CharField(max_length=50)

    # def Get_Name(self):
    #     return self.name
    def Get_Name(self):
        return self.name
    # def Get_Name(self, longitude, latitude):
    #     cursor = self.connection.cursor()
    #     query = """
    #     SELECT name FROM place 
    #     WHERE longitude = %s AND latitude = %s
    #     """
    #     cursor.execute(query, (longitude, latitude))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     if result:
    #         return result[0]
    #     else:
    #         return "No place found with the provided coordinates."

    # def Get_location_longitude(self):
    #     return self.longitude
    def Get_Longitude(self):
        return self.longitude
    # def Get_location_longitude(self, name):
    #     cursor = self.connection.cursor()
    #     query = "SELECT longitude FROM place WHERE name = %s"
    #     cursor.execute(query, (name,))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     if result:
    #         return result[0]
    #     else:
    #         return "No place found with this name."

    def Get_Latitude(self):
        return self.latitude

    def Get_City(self):
        return self.city

    def Set_Name(self, name):
        # update, input longi&lati, reset name
        self.name = name
        # cursor = self.connection.cursor()
        # query = "SELECT name, longitude, latitude, city FROM places WHERE name = %s"
        # cursor.execute(query, (name,))
        # result = cursor.fetchone()
        # cursor.close()
        # if result:
        #     self.name, self.longitude, self.latitude, self.city = result

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


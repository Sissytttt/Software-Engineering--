from django.db import models
from django.utils import timezone

from .BusinessOwner import BusinessOwner
from .place import Place
from .client import Client

class Event(models.MOdel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    place = models.ForeignKey(
        Place,
        on_delete = models.CASCADE,
    )
    business_owner = models.ForeignKey(
        BusinessOwner,
        on_delete = models.CASCADE,
    )
    start_time = models.DateTimeField(editable=True)
    end_time = models.DateTimeField(editable=True)
    description = models.TextField()
    max_ppl = models.IntegerField()
    current_ppl = models.IntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=4)
    avg_price = models.DecimalField(max_digits=10, decimal_places=4)
    # to be added
    EVENT_CHOICE = [
        ('dining', 'Dining'),
        ('outdoor', 'Outdoor'),
        ('party', 'Party'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('other', 'Other'),]
    event_type = models.TextChoices(EVENT_CHOICE)
    

    def get_name(self):
        return self.name
        
    def get_place(self):
        return self.place

    def get_business_owner(self):
        return self.business_owner

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_description(self):
        return self.description

    def get_max_ppl(self):
        return self.max_ppl

    def get_current_ppl(self):
        return self.current_ppl

    def get_score(self):
        return self.score

    def get_event_type(self):
        return self.event_type

    def get_avg_arice(self):
        return self.avg_price

    def set_business_owner(self, business_owner):
        self.business_owner = business_owner

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_description(self, description):
        self.description = description

    def set_max_ppl(self, max_ppl):
        self.max_ppl = max_ppl

    def set_type(self, event_type):
        self.event_type = event_type

    def update_current_ppl(self, current_ppl):
        self.current_ppl = current_ppl

    def Update_Score_And_Spending(self, event_review):
        # Implement this method based on your requirements
        pass

    def check_full(self):
        return self.current_ppl >= self.max_ppl


class rsvp(models.Model):

    id = models.AutoField(primary_key=True)

    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )

    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )


# class Event:
#     def __init__(self, host, user, password, database):
#         self.connection = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=database
#         )
#         self.name = None
#         self.business_owner = None # connect
#         self.start_time = None
#         self.end_time = None
#         self.description = None
#         self.max_ppl = None
#         self.current_ppl = None
#         self.score = None
#         self.avg_price = None
#         self.type = None
#         self.place = None # ? connect to place class


#     def Get_Name(self, ): # 通过什么找名字？
#         return self.name
        
#     def Get_Place(self, name):
#         cursor = self.connection.cursor()
#         query = """
#         SELECT place FROM event 
#         WHERE name = %s
#         """
#         cursor.execute(query, (name))
#         result = cursor.fetchone()
#         cursor.close()
#         if result:
#             return result[0]
#         else:
#             return "No event found"

#     def Get_Business_Owner(self, name):
#         cursor = self.connection.cursor()
#         query = """
#         SELECT business_owner FROM event 
#         WHERE name = %s
#         """
#         cursor.execute(query, (name))
#         result = cursor.fetchone()
#         cursor.close()
#         if result:
#             return result[0]
#         else:
#             return "No event found"

#     def Get_Start_Time(self, name):
#         cursor = self.connection.cursor()
#         query = """
#         SELECT start_time FROM event 
#         WHERE name = %s
#         """
#         cursor.execute(query, (name))
#         result = cursor.fetchone()
#         cursor.close()
#         if result:
#             return result[0]
#         else:
#             return "No event found"

#     def Get_End_Time(self):
#         return self.end_time

#     def Get_Description(self):
#         return self.description

#     def Get_Max_Ppl(self):
#         return self.max_ppl

#     def Get_Current_Ppl(self):
#         return self.current_ppl

#     def Get_Score(self):
#         return self.score

#     def Get_Type(self):
#         return self.event_type

#     def Get_Avg_Price(self):
#         return self.avg_price

#     def Set_Business_Owner(self, business_owner):
#         self.business_owner = business_owner

#     def Set_Start_Time(self, start_time):
#         self.start_time = start_time

#     def Set_End_Time(self, end_time):
#         self.end_time = end_time

#     def Set_Description(self, description):
#         self.description = description

#     def Set_Max_Ppl(self, max_ppl):
#         self.max_ppl = max_ppl

#     def Set_Type(self, event_type):
#         self.event_type = event_type

#     def Update_Current_Ppl(self, ppl):
#         self.current_ppl = ppl

#     def Update_Score_And_Spending(self, event_review):
#         # Implement this method based on your requirements
#         pass

#     def Check_Full(self):
#         return self.current_ppl >= self.max_ppl

from django.db import models

from .event import Event
from .client import Client # to implement client

class Event_Review(models.MOdel):
    id = models.AutoField(primary_key=True, serialize = False)

    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE
    )

    client = models.ForeignKey(
        Client,
        on_delete = models.CASCADE
    )

    content = models.TextField()

    RATING_CHOICE = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]
    rating = models.IntegerChoice(RATING_CHOICE)

    creation_date = models.DateTimeField(default=timezone.now)


    def get_content(self):
        return self.content
        
    def get_rating(self):
        return self.rating

    def set_content(self, content):
        self.content = content
        
    def set_rating(self, new_rating):
        if 1 <= new_rating <= 5:
            if type(new_rating) == int:
                self.rating = new_rating
            else:
                # adjust type
                self.rating = int(new_rating)
        else:
            # clip rating
            self.rating = min(5,max(1,new_rating))
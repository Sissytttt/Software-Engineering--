from models import BusinessOwner, Place, Event #BO
from django.test import TestCase
from django.contrib.auth.models import User as user_bo #authenti
from datetime import time

class BOTestCase(TestCase):
    def setUp(self):
        bo1 = user_bo.objects.create_user( #authenti
            email = "test1@nyu.edu",
            name = "test_bo_1",
            password = "123"
        )
        self.test_bo1 = User.objects.create( # 
            phone_number = 1234567,
            city = "Shanghai"
        )
        self.place1 = Place.objects.create(
            id = 1,
            name = "Yu Garden",
            location_longitude = 31.2277,
            location_latitude = 121.4923,
            city = "Shanghai"
        )

    def test_post_event(self):
        """
        test case: bussiness owner 1 create a new event, we are veritfying if the event is created with the correct information and the poster
        inputs: info of the new event (the event called "visit Yu Garden", with start time from 2024-04-03 08:30:0 to end time 2024-04-04 20:30:0, max ppl of 12, "outdoor" type, at place "Yu Garden")
        expected outputs: no error output
        preconditions or assumptions: none
        """
        self.test_bo1.Post_Event(name="visit Yu Garden", start_time=datetime("2024", "4", "3", "8", "30", "0"), end_time=datetime("2024", "4", "4", "20", "30", "0"), max_ppl=12, event_type="outdoor", Place=self.place1)
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.name, "visit Yu Garden")
        self.assertEqual(event.business_owner, self.test_bo1)
        self.assertEqual(event.start_time, datetime("2024", "4", "3", "8", "30", "0"))
        self.assertEqual(event.end_time, datetime("2024", "4", "4", "20", "30", "0"))
        self.assertEqual(event.max_ppl, 12)
        self.assertEqual(event.event_type, "entrance ticket")
        self.assertEqual(event.place, self.place1)
        self.assertEqual(event.ppl_reviewed, 0)
    
    
    def test_delete_event(self):
        """
        test case: bussiness owner 1 delete a certain event, we are veritfying if the event is correctly deleted
        inputs: the event that needs to be deleted (visit Yu Garden)
        expected outputs: no error output
        preconditions or assumptions: none
        """
        self.test_bo1.Post_Event(name="visit Yu Garden", start_time=datetime("2024", "4", "3", "8", "30", "0"), end_time=datetime("2024", "4", "4", "20", "30", "0"), max_ppl=12, event_type="outdoor", Place=self.place1)
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.name, "visit Yu Garden")
        self.test_bo1.Delete_Event(event)
        with self.assertRaises(event.DoesNotExist):
            Event.objects.get(author=self.test_bo1)
    
    def test_search_place(self):
        """
        test case: bussiness owner 1 search for a place in the database with its name, we are veritfying if the place can be found
        inputs: the place's name and located city: (The Bund, Shanghai), (Yu Garden, Shanghai)
        expected outputs: no error output
        preconditions or assumptions: none
        """
        # test non exisiting place
        places_qobjects1 = self.test_user1.Search_Place(name="The Bund",city="Shanghai")
        num_places1 = places_qobjects1.count()
        self.assertEqual(num_places1,0)
        
        # test existing place, and test its name and city match
        places_qobjects2 = self.test_user1.Search_Place(name="Yu Garden", city="Shanghai")
        num_places2 = places_qobjects2.count()
        self.assertEqual(num_places2,1)
        for place in places_qobjects2:
          self.assertEqual(place.name,"Yu Garden")
          self.assertEqual(place.city,"Shanghai")
      
    
    def test_search_event(self):
        """
        test case: the user is searching either a "false event" that does not exist or a event that existed ("visit Yu Garden" event). 
                   We are checking whether the system can identify the existance of the event and return the correct event the user is searching
        inputs: the event's name and located city: (false event, Shanghai), (visit Yu Garden, Shanghai)
        expected outputs: no error output
        preconditions or assumptions: none
        """
        # test non exisiting event
        events_qobjects1 = self.test_user1.Search_Event(name="false event", city="Shanghai", Etype="false type")
        num_events1 = events_qobjects1.count()
        self.assertEqual(num_events1,0)
        
        # test existing event, and test its name and city match
        events_qobjects1 = self.test_user1.Search_Event(name="visit Yu Garden", city="Shanghai", Etype="outdoor")
        num_events2 = events_qobjects1.count()
        self.assertEqual(num_events2,1)
        for event in events_qobjects2:
          self.assertEqual(event.name,"visit Yu Garden")
          self.assertEqual(event.city,"Shanghai")
          self.assertEqual(event.event_type,"outdoor")
        

from models import BusinessOwner, Place, Event, Event_Review, Client
from django.test import TestCase
from django.contrib.auth.models import User as user_bo #authenti
from datetime import time

class EventTestCase(TestCase):
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
        bo2 = user_bo.objects.create_user(
            email = "test2@nyu.edu",
            name = "test_bo_2",
            password = "123"
        )
        self.test_bo2 = User.objects.create(
            phone_number = 7654321,
            city = "Shanghai"
        )
        client1 = user_bo.objects.create_user(
            email = "test3@nyu.edu",
            name = "test_client_1",
            password = "123"
        )
        self.client1 = Client.object.create(
           phone_number = 1234568
           city = "Shanghai"
        )
        self.place1 = Place.objects.create(
            name = "Yu Garden",
            location_longitude = 31.2277,
            location_latitude = 121.4923,
            city = "Shanghai"
        )
        self.event1 = Event.objects.create(
           name = "visit Yu Garden",
           place = self.place1,
           business_owner = self.test_bo1,
           start_time = datetime("2024", "4", "3", "8", "30", "0"),
           end_time = datetime("2024", "4", "4", "20", "30", "0"),
           description = "entrance ticket",
           max_ppl = 12,
           current_ppl = 0,
           score = 5,
           avg_price = 15,
           event_type = "outdoor",
           ppl_reviewed = 1,
        )
        self.event_review1 = Event_Review.objects.create(
           event = self.event1,
           client = self.client1,
           content = "not satisfying",
           rating = 1,
           price = 45,
           creation_date = datetime("2024", "4", "4", "14", "30", "0")
        )
        
        
    def test_set_business_owner(self):
        """
        test case: update the busines owner of this event, we want to verify if the updated event got the correct new business owner
        inputs: new busines owner: test_bo2
        expected outputs: no error output
        preconditions or assumptions: none
        """
        event = Event.objects.get(business_owner=self.test_bo1)
        self.test_bo1.set_business_owner(test_bo2)
        self.assertEquaL(event.business_owner,test_bo2)

    def test_set_start_time(self):
        """
        test case: update the start time of this event, we want to verify if the updated event got the correct new start time
        inputs: new start time: 2024-04-04 8:30:0
        expected outputs: no error output
        preconditions or assumptions: none
        """
        self.event1.set_end_time(end_time=datetime("2024", "4", "4", "8", "30", "0")) # change date
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.start_time, datetime("2024", "4", "4", "8", "30", "0")) # also changed
    
    def test_set_end_time(self):
        """
        test case: update the end time of this event, we want to verify if the updated event got the correct new end time
        inputs: new end time: 2024-04-05 20:30:0
        expected outputs: no error output
        preconditions or assumptions: none
        """
        self.event1.set_end_time(end_time=datetime("2024", "4", "5", "20", "30", "0")) # change date
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.end_time, datetime("2024", "4", "5", "20", "30", "0")) # also changed
      
    def test_set_description(self):
        """
        test case: update the description of this event, we want to verify if the updated event got the correct new description
        inputs: new description: this is a new description
        expected outputs: no error output
        preconditions or assumptions: none
        """
        event = Event.objects.get(business_owner=self.test_bo1)
        event.set_description("this is a new description")
        self.assertEqual(event.description, "this is a new description")
        
    def test_set_max_ppl(self):
        """
        test case: update the max ppl allowed of this event, we want to verify if the updated max ppl is what we desired
        inputs: new test max ppl: 30
        expected outputs: no error output
        preconditions or assumptions: none
        """
        event = Event.objects.get(business_owner = self.test_bo1)
        self.event1.set_max_ppl(30) # change max ppl
        self.assertEqual(event.max_ppl, 30)
    
    def test_set_type(self):
        """
        test case: update the type of this event, we want to verify if the updated type is what we desired
        inputs: new event type: party
        expected outputs: no error output
        preconditions or assumptions: none
        """
        self.event1.set_type(event_type="party") # change type
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.event_type, "party") # also changed
        
    def test_update_current_ppl(self):
        """
        test case: update the current ppl of this event, we want to verify if the updated number of ppl is what we desired
        inputs: new current people: 11
        expected outputs: no error output
        preconditions or assumptions: assume the newly updated people number will not exceed the max people allowed
        """
        self.event1.update_current_ppl(current_ppl=11) # change current_ppl
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.current_ppl, 11) # also changed
        
    def test_update_score_and_spending(self):
        """
        test case: update the rate and avg price of attending the event, we want to verify if the update is what we desired
        inputs: new score, new avg price
        expected outputs: no error output
        preconditions or assumptions: none
        """
        self.event1.Update_Score_And_Spending(event_review=self.event_review1) # change current_ppl
        event = Event.objects.get(business_owner=self.test_bo1)
        self.assertEqual(event.score, 3.0) # also changed
        self.assertEqual(event.avg_price, 30.0) # also changed
        
    def test_check_full(self):
        """
        test case: test if check full works well under both full and non full case.
        inputs: none
        expected outputs: no error output
        preconditions or assumptions: the first test will not exceed max ppl, but the second should exceed max ppl, so both expected to return no error
        """
        event = Event.objects.get(business_owner=self.test_bo1)
        # test not full
        event.update_current_ppl(current_ppl=1)
        self.assertEqual(event.check_full(), False)
        # test a full case
        event.update_current_ppl(current_ppl=1000)
        self.assertEqual(event.check_full(), True)
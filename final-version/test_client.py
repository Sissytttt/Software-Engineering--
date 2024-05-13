import unittest
from main import app


class TestClientApp(unittest.TestCase):
    """
    Unit tests for the business owner part of the app, starting from register.

    Test cases for various functionalities including registration,
        login, event creation, event search, event modification, and event deletion.
        And all corner cases are covered in the test.
    """
        
    def setUp(self):
        """
        Set up test environment before each test case.

        Configures the application for testing and initializes a test client.
        """
        app.testing = True
        self.app = app.test_client()


    def tearDown(self):
        """
        Clean up test environment after each test case.

        Performs any necessary cleanup after each test case execution.
        """
        pass

    # start testing --------------------------------------------------

    def test_registerAuth_client(self):
        """
        Test case for client registration authentication.

        Simulates a registration attempt and checks if the response status
            code is as expected.
        """
        response = self.app.post('/register_auth_client', data=dict(
            email='test@example.com',
            company_name='Test Company',
            name='Test User',
            password='password',
            phone_number='1234567890',
            city='Test City'
        ))
        self.assertEqual(response.status_code, 200)


    def test_registerAuth_duplicate_client(self):
        """
        Test case for corner case client registration authentication,
            when a duplicate name is registered, the app will not crash.

        Simulates a registration attempt and checks if the response status
            code is as expected.
        """
        response = self.app.post('/register_auth_client', data=dict(
            email='test@example.com',
            company_name='Test Company',
            name='Test User',
            password='password',
            phone_number='1234567890',
            city='Test City'
        ))
        self.assertEqual(response.status_code, 200)


    def test_loginAuth_client(self):
        """
        Test case for client login authentication.

        Simulates a login attempt and checks if the response status code
        is as expected.
        """
        response = self.app.post('/login_auth_client', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_loginAuth_client_false_credential(self):
        """
        Test case for corner case when client login input false credential,
            the app will not crash.

        Simulates a login attempt and checks if the response status code
        is as expected.
        """
        response = self.app.post('/login_auth_client', data=dict(
            email='t@e.com',
            password='fasle_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_client_search_event_form(self):
        # assume a logged-in session
        """
        Test case for searching events by a client.

        Simulates an event search attempt and checks if the response
        status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_search_event_form', data=dict(
            name='New event',
            time='2000-05-14',
            score = '0',
            price = '10'
        ))
        self.assertEqual(response.status_code, 200)


    def test_client_search_event_form_no_such_event(self):
        # assume a logged-in session
        """
        Test case for corner case when searching events that doesn't exist,
            the app will not crash.

        Simulates an event search attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_search_event_form', data=dict(
            name='No such event',
            time='2000-05-14',
            score = '0',
            price = '10'
        ))
        self.assertEqual(response.status_code, 200)


    def test_client_register_event(self):
        # assume a logged-in session
        """
        Test case for registering an event.

        Simulates an event register attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/register_event', data=dict(
            event_id='7'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_register_event_again(self):
        # assume a logged-in session
        """
        Test case for registering an event.

        Simulates an event register attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/register_event', data=dict(
            event_id='7'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_view_event_bo(self):
        # assume a logged-in session
        """
        Test case for viewing the business owner profile of an event.

        Simulates an view bo profile attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_view_bo', data=dict(
            event_id='7'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_follow_bo(self):
        # assume a logged-in session
        """
        Test case for viewing the business owner profile of an event.

        Simulates an follow bo attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_follow_bo', data=dict(
            bo_id='1'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_follow_bo_again(self):
        # assume a logged-in session
        """
        Test case for corner case when the business owner is already followed by the client,
            the app will not crash.

        Simulates an follow bo attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_follow_bo', data=dict(
            bo_id='1'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_search_place_form(self):
        # assume a logged-in session
        """
        Test case for searching places by a client.

        Simulates an place search attempt and checks if the response
        status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_search_place_form', data=dict(
            name='Yu Garden',
            city='Shanghai'
        ))
        self.assertEqual(response.status_code, 200)
    
    def test_client_search_place_form_no_such_place(self):
        # assume a logged-in session
        """
        Test case for corner case when searching places that doesn't exist,
            the app will not crash.

        Simulates an place search attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_search_place_form', data=dict(
            name='No such event',
            city='Test city'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_label_place(self):
        # assume a logged-in session
        """
        Test case for labeling a place into an event's map.

        Simulates an label place attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_label_place_to_map', data=dict(
            place_id='7'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_label_place_again(self):
        # assume a logged-in session
        """
        Test case for corner case when the place is already added to the client's map,
            the app will not crash.

        Simulates an label place attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_label_place_to_map', data=dict(
            place_id='7'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_view_posted_reviews(self):
        """
        Test case for viewing reviews posted by a client.

        Simulates viewing posted reviews and checks if the response
            status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.get('/client_view_review')
        self.assertEqual(response.status_code, 200)

    def test_client_view_posted_reviews_delete_reviews(self):
        """
        Test case for deleting reviews posted by a client.

        Simulates deleting posted reviews and checks if the response
            status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_delete_review', data=dict(
            review_id='2'
        ))
        self.assertEqual(response.status_code, 200)

    def test_client_view_event(self):
        """
        Test case for viewing any events a client has RSVPed.

        Simulates viewing rsvped events and checks if the response
            status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_view_event')
        self.assertEqual(response.status_code, 200)

    def test_client_post_review(self):
        # assume a logged-in session
        """
        Test case when the client wants to post a review for an event.

        Simulates an post review attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_post_review', data=dict(
            event_id='7',
            content='Test content',
            rating='5'
        ))
        self.assertEqual(response.status_code, 200)

    def test_cancle_register(self):
        """
        Test case when the client wants to cancle registering an event.

        Simulates an post review attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'
        response = self.app.post('/client_unrsvp_event', data=dict(
            event_id='7'
        ))
        self.assertEqual(response.status_code, 200)
    
    def test_get_following(self):
        """
        Test case when the client wants to get the business owners he is following.

        Simulates an post review attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'
        response = self.app.post('/client_view_follow')
        self.assertEqual(response.status_code, 200)
    
    def test_unfollow(self):
        """
        Test case when the client wants to unfollow a business owner.

        Simulates an post review attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_unfollow_bo', data=dict(
            bo_id='1',
        ))
        self.assertEqual(response.status_code, 200)

    def test_view_map(self):
        """
        Test case when the client wants to view the places he labeled.

        Simulates an post review attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/view_map')
        self.assertEqual(response.status_code, 200)

    def test_unlabel(self):
        """
        Test case when the client wants to unlabel a place.

        Simulates an post review attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/client_unlike_place', data=dict(
            place_id='7',
        ))
        self.assertEqual(response.status_code, 200)


    
# start test
if __name__ == '__main__':
    '''
    Expected result:

    Ran 11 tests in ...s

    OK
    '''
    unittest.main()

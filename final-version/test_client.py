import unittest
from main import app


class TestBoApp(unittest.TestCase):
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

    def test_registerAuth_bo(self):
        """
        Test case for business owner registration authentication.

        Simulates a registration attempt and checks if the response status
            code is as expected.
        """
        response = self.app.post('/register_auth_bo', data=dict(
            email='test@example.com',
            company_name='Test Company',
            name='Test User',
            password='password',
            phone_number='1234567890',
            city='Test City'
        ))
        self.assertEqual(response.status_code, 200)


    def test_registerAuth_duplicate_bo(self):
        """
        Test case for corner case business owner registration authentication,
            when a duplicate name is registered, the app will not crash.

        Simulates a registration attempt and checks if the response status
            code is as expected.
        """
        response = self.app.post('/register_auth_bo', data=dict(
            email='test@example.com',
            company_name='Test Company',
            name='Test User',
            password='password',
            phone_number='1234567890',
            city='Test City'
        ))
        self.assertEqual(response.status_code, 200)


    def test_loginAuth_business_owner(self):
        """
        Test case for business owner login authentication.

        Simulates a login attempt and checks if the response status code
        is as expected.
        """
        response = self.app.post('/login_auth_bo', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_loginAuth_business_owner_false_credential(self):
        """
        Test case for corner case when business owner login input false credential,
            the app will not crash.

        Simulates a login attempt and checks if the response status code
        is as expected.
        """
        response = self.app.post('/login_auth_bo', data=dict(
            email='t@e.com',
            password='fasle_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_bo_create_event_form(self):
        """
        Test case for creating an event by a business owner.

        Simulates an event creation attempt and checks if the response
            status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/bo_create_event_form', data=dict(
            e_name='New Event',
            e_time='2024-05-14',
            e_descript='Description',
            e_max_ppl='100',
            e_price='20',
            e_place='Yu Garden'
        ))
        self.assertEqual(response.status_code, 200)


    def test_bo_search_event_form(self):
        # assume a logged-in session
        """
        Test case for searching events by a business owner.

        Simulates an event search attempt and checks if the response
        status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/bo_search_event_form', data=dict(
            name='New event',
            time='2000-05-14',
            score = '0',
            price = '10'
        ))
        self.assertEqual(response.status_code, 200)


    def test_bo_search_event_form_no_such_event(self):
        # assume a logged-in session
        """
        Test case for corner case when searching events that doesn't exist,
            the app will not crash.

        Simulates an event search attempt and checks if the response
            status code is as expected.
        """
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/bo_search_event_form', data=dict(
            name='No such event',
            time='2000-05-14',
            score = '0',
            price = '10'
        ))
        self.assertEqual(response.status_code, 200)


    def test_bo_view_my_event(self):
        """
        Test case for viewing events owned by a business owner.

        Simulates viewing owned events and checks if the response
            status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.get('/bo_view_event')
        self.assertEqual(response.status_code, 200)


    def test_bo_modify_event_form(self):
        """
        Test case for modifying an event by a business owner.

        Simulates modifying an event and checks if the response
            status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/bo_modify_event_form', data=dict(
            event_name='New Event',
            parameter_to_modify='score',
            new_value='1' ,
            new_time = '2024-5-11' 
        ))
        self.assertEqual(response.status_code, 200)


    def test_bo_modify_event_duplicate_name_form(self):
        """
        Test case for modifying an event with a duplicate name by a business owner, 
            encountering the corner case will not crash the app.

        Simulates modifying an event with a name that already exists and checks
            if the response status code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/bo_modify_event_form', data=dict(
            event_name='New Event',
            parameter_to_modify='name',
            new_value='New Event' ,
            new_time = '2024-5-11' 
        ))
        self.assertEqual(response.status_code, 200)


    def test_bo_delete_event_form(self):
        """
        Test case for deleting an event by a business owner.
            Since our front end only displays events that's available,
            so no corner case in delete event, like delete an unexisted event,
            as such event will not be displayed to bo on front end.

        Simulates deleting an event and checks if the response status
            code is as expected.
        """
        # assume a logged-in session
        with self.app.session_transaction() as session:
            session['email'] = 'test@example.com'

        response = self.app.post('/bo_delete_event_form', data=dict(
            event_id='1'
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

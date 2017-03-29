import json
import unittest

from app import current_app as app
from app.helpers.data import update_role_to_admin
from tests.unittests.api.utils import create_event, create_services, get_path
from tests.unittests.auth_helper import register, login
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class PaginatedApiTestCase:
    """
    Base class to inherit from when creating a paginated Api TestCase
    """

    def __init__(self):
        pass

    def _test_model(self, param):
        pass

    def test_track_api(self):
        self._test_model('track')

    def test_microlocation_api(self):
        self._test_model('microlocation')

    def test_session_api(self):
        self._test_model('session')

    def test_speaker_api(self):
        self._test_model('speaker')

    def test_sponsor_api(self):
        self._test_model('sponsor')


class TestGetApiPaginated(OpenEventTestCase, PaginatedApiTestCase):
    """
    Basic test for Paginated APIs
    """

    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            create_event(creator_email=u'test@example.com')

    def _test_model(self, name):
        """
        Tests the 404 response, then add item
        and test the success response
        """
        login(self.app, u'test@example.com', u'test')
        path = get_path(1, name + 's', 'page')
        response = self.app.get(path, follow_redirects=True)
        # check for 404 in no data
        self.assertEqual(response.status_code, 404)
        # add single data
        with app.test_request_context():
            create_services(1)
        response = self.app.get(path, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test' + str(name).title(), response.data)


class TestGetApiPaginatedUrls(OpenEventTestCase, PaginatedApiTestCase):
    """
    Test the next and previous urls returned in the
    paginated APIs
    """

    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            # User must be part of the staff to access listed events
            update_role_to_admin({'admin_perm': 'isAdmin'}, user_id=1)

            event_id = create_event(creator_email=u'test@example.com')
            create_services(event_id)

    def _json_from_url(self, url):
        """
        Helper function to return json from the url
        """
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.data)

    def _test_model(self, name):
        """
        Tests -
        1. When just one item, check if next and prev urls are empty
        2. When one more item added, limit results to 1 and see if
            next is not empty
        3. start from position 2 and see if prev is not empty
        """
        login(self.app, u'test@example.com', u'test')
        if name == 'event':
            path = get_path('page')
        else:
            path = get_path(1, name + 's', 'page')
        data = self._json_from_url(path)
        self.assertEqual(data['next'], '')
        self.assertEqual(data['previous'], '')
        # add second service
        with app.test_request_context():
            create_event(name='TestEvent2')
            create_services(1)
        data = self._json_from_url(path + '?limit=1')
        self.assertIn('start=2', data['next'])
        self.assertEqual(data['previous'], '')
        # check from start=2
        data = self._json_from_url(path + '?start=2')
        self.assertIn('limit=1', data['previous'])
        self.assertEqual(data['next'], '')
        self.assertIn('http', data['previous'])  # check absolute link

    def test_event_api(self):
        self._test_model('event')


class TestGetApiPaginatedEvents(OpenEventTestCase):
    """
    Test Paginated GET API for Events
    """

    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            # User must be part of the staff to access listed events
            update_role_to_admin({'admin_perm': 'isAdmin'}, user_id=1)

    def test_api(self):
        login(self.app, u'test@example.com', u'test')
        path = get_path('page')
        response = self.app.get(path)
        self.assertEqual(response.status_code, 404, msg=response.data)
        with app.test_request_context():
            create_event()
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestEvent', response.data)

    def test_api_filters(self):
        with app.test_request_context():
            create_event(creator_email=u'test@example.com')
        path = get_path('page') + '?location=r@nd0m'
        resp = self.app.get(path)
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()

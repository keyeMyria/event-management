import unittest

from app import current_app as app
from tests.unittests.api.utils import get_path, create_event
from tests.unittests.auth_helper import register, login
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class TestGetApiNonExistingEvent(OpenEventTestCase):
    """Test 404 response code for non existing Event
    """

    def test_event_api(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            login(self.app, u'test@example.com', u'test')
            # Non existing event
            event_id = 1
            path = get_path(event_id)
            response = self.app.get(path)
            self.assertEqual(response.status_code, 404)
            self.assertIn('does not exist', response.data)


class TestGetApiNonExistingServices(OpenEventTestCase):
    """Test 404 response code for non existing services.
    Services include Session, Track, etc. (everything except Event)
    """

    def setUp(self):
        """Create Event but don't define services for it.
        """
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            # Created event will have id=1
            create_event(creator_email=u'test@example.com')

    def _test_path(self, path):
        """Helper function.
        Test response for 404 status code. Also test if response body
        contains 'does no exist' string.
        """
        with app.test_request_context():
            login(self.app, u'test@example.com', u'test')
            response = self.app.get(path)
            self.assertEqual(response.status_code, 404)
            self.assertIn('does not exist', response.data)

    def test_microlocation_api(self):
        path = get_path(1, 'microlocations', 1)
        self._test_path(path)

    def test_track_api(self):
        path = get_path(1, 'tracks', 1)
        self._test_path(path)

    def test_session_api(self):
        path = get_path(1, 'sessions', 1)
        self._test_path(path)

    def test_speaker_api(self):
        path = get_path(1, 'speakers', 1)
        self._test_path(path)

    def test_sponsor_api(self):
        path = get_path(1, 'sponsors', 1)
        self._test_path(path)


if __name__ == '__main__':
    unittest.main()

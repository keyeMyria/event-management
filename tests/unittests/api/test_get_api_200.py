import unittest

from app import current_app as app
from tests.unittests.api.utils import get_path, create_event, create_services
from tests.unittests.auth_helper import register, logout
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class TestGetApi(OpenEventTestCase):
    """Tests for version 2 GET APIs
    """

    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            # `event_id` is going to be 1
            event_id = create_event(creator_email=u'test@example.com')
            # Associate services to event_id
            create_services(event_id)

    def _test_path(self, path, *strings):
        """Helper function.
        Test response for 200 status code. Also test if response body
        contains event/service name.
        """
        with app.test_request_context():
            response = self.app.get(path, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            for string in strings:
                self.assertIn(string, response.data)

    def test_event_api(self):
        path = get_path(1)
        self._test_path(path, 'TestEvent')

    def test_track_api(self):
        path = get_path(1, 'tracks', 1)
        self._test_path(path, 'TestTrack_1')

    def test_microlocation_api(self):
        path = get_path(1, 'microlocations', 1)
        self._test_path(path, 'TestMicrolocation_1')

    def test_session_api(self):
        path = get_path(1, 'sessions', 1)
        self._test_path(path, 'TestSession_1')

    def test_speaker_api(self):
        path = get_path(1, 'speakers', 1)
        # logged in and check
        self._test_path(path, 'TestSpeaker_1', 'email', 'mobile')
        # logged out, private fields not present
        logout(self.app)
        resp = self.app.get(path)
        self.assertNotIn('email', resp.data)
        self.assertNotIn('mobile', resp.data)

    def test_sponsor_api(self):
        path = get_path(1, 'sponsors', 1)
        self._test_path(path, 'TestSponsor_1')


if __name__ == '__main__':
    unittest.main()

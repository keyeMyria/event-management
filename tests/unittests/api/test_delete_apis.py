import json
import unittest

from app import current_app as app
from tests.unittests.api.utils import create_event, get_path, Event, Session
from tests.unittests.api.utils_post_data import *
from tests.unittests.auth_helper import register, login
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class TestDeleteApi(OpenEventTestCase):
    """
    Test Delete APIs for 200 (successful) status codes
    """

    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            create_event(creator_email=u'test@example.com')

    def _login_user(self):
        """
        Registers an email and logs in.
        """
        with app.test_request_context():
            login(self.app, u'test@example.com', u'test')

    def _test_model(self, name, data):
        """
        Logs in a user and creates model.
        Tests for 200 status on deletion and for the deleted object.
        Tests that the deleted object no longer exists.
        """
        self._login_user()
        path = get_path() if name == 'event' else get_path(1, name + 's')
        response = self.app.post(
            path,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

        path = get_path(1) if name == 'event' else get_path(1, name + 's', 1)
        response = self.app.delete(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test' + str(name).title(), response.data)

        response = self.app.get(path)
        self.assertEqual(response.status_code, 404)
        self.assertIn('does not exist', response.data)

    def _test_trashed(self, model):
        with app.test_request_context():
            item = model.query.get(1)
            self.assertNotEqual(item, None)
            self.assertEqual(item.in_trash, True)

    def test_event_api(self):
        self._test_model('event', POST_EVENT_DATA)
        self._test_trashed(Event)

    def test_track_api(self):
        self._test_model('track', POST_TRACK_DATA)

    def test_microlocation_api(self):
        self._test_model('microlocation', POST_MICROLOCATION_DATA)

    def test_session_api(self):
        self._test_model('session', POST_SESSION_DATA)
        self._test_trashed(Session)

    def test_speaker_api(self):
        self._test_model('speaker', POST_SPEAKER_DATA)

    def test_sponsor_api(self):
        self._test_model('sponsor', POST_SPONSOR_DATA)

    def test_social_link_api(self):
        self._login_user()
        # Create a social link
        path = get_path(1, 'links')
        data = POST_SOCIAL_LINK_DATA
        response = self.app.post(
            path,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

        # Delete the social link
        path = get_path(1, 'links', 1)
        response = self.app.delete(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestSocialLink', response.data)

        # Test if it's in event-links
        path = get_path(1, 'links')
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('TestSocialLink', response.data)

    def test_session_type_api(self):
        self._login_user()
        # Create a session type
        path = get_path(1, 'sessions', 'types')
        data = POST_SESSION_TYPE_DATA
        response = self.app.post(
            path,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 201)

        # Delete the session type
        path = get_path(1, 'sessions', 'types', 1)
        response = self.app.delete(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestSessionType', response.data)

        # Test if it's in session types
        path = get_path(1, 'sessions', 'types')
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('TestSessionType', response.data)


if __name__ == '__main__':
    unittest.main()

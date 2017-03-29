import unittest

from tests.unittests.api.utils import get_path
from tests.unittests.api.utils_post_data import *

from test_post_api import TestPostApiBase


class ApiValidationTestCase():
    """
    Base class for testing api validation
    NOTE - validates only for custom fields like email, url, color, datetime
    """
    def _test_model(self, name, data, fields=[]):
        pass

    def test_event_api(self):
        return self._test_model(
            'event',
            POST_EVENT_DATA,
            ['email', 'logo', 'event_url', 'background_image',
                'type', 'topic', 'privacy', 'sub_topic', 'state', 'has_session_speakers']
        )

    def test_speaker_api(self):
        return self._test_model(
            'speaker',
            POST_SPEAKER_DATA,
            ['photo', 'email', 'website']
        )

    def test_sponsor_api(self):
        return self._test_model('sponsor', POST_SPONSOR_DATA, ['url', 'logo'])

    def test_track_api(self):
        return self._test_model(
            'track',
            POST_TRACK_DATA,
            ['track_image_url', 'color']
        )


class TestPostApiValidation(TestPostApiBase, ApiValidationTestCase):
    """
    Tests the input validation in POST API
    """
    def _test_model(self, name, data, fields=None):
        """
        Sets a random value to each of the :fields in :data and makes
        sure POST request failed
        """
        if fields is None:
            fields = []
        path = get_path() if name == 'event' else get_path(1, name + 's')
        self._login_user()
        for field in fields:
            data_copy = data.copy()
            data_copy[field] = 'r@nd0m_g00d_for_n0thing_v@lue'
            response = self.post_request(path, data_copy)
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

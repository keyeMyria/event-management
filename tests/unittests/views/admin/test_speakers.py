import unittest

from tests.unittests.object_mother import ObjectMother
from app import current_app as app
from app.helpers.data import save_to_db
from flask import url_for

from tests.unittests.views.view_test_case import OpenEventViewTestCase


class TestSpeakers(OpenEventViewTestCase):

    def test_speakers_list(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            url = url_for('event_speakers.index_view', event_id=event.id)
            rv = self.app.get(url, follow_redirects=True)
            self.assertTrue("Speakers" in rv.data, msg=rv.data)

    def test_speaker_delete(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            speaker = ObjectMother.get_speaker()
            speaker.event_id = event.id
            save_to_db(speaker, "Session Saved")
            url = url_for('event_speakers.delete', event_id=event.id, speaker_id=speaker.id)
            rv = self.app.get(url, follow_redirects=True)
            self.assertTrue("deleted" in rv.data, msg=rv.data)

    def test_speaker_view(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            speaker = ObjectMother.get_speaker()
            speaker.event_id = event.id
            save_to_db(speaker, "Speaker saved")
            custom_forms = ObjectMother.get_custom_form()
            custom_forms.event_id = event.id
            save_to_db(custom_forms, "Custom forms Saved")
            url = url_for('event_speakers.edit_view', event_id=event.id, speaker_id=speaker.id)
            rv = self.app.get(url, follow_redirects=True)
            self.assertTrue("name" in rv.data, msg=rv.data)

    def test_speaker_edit(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            speaker = ObjectMother.get_speaker()
            speaker.event_id = event.id
            save_to_db(speaker, "Speaker saved")
            custom_forms = ObjectMother.get_custom_form()
            custom_forms.event_id = event.id
            save_to_db(custom_forms, "Custom forms Saved")
            url = url_for('event_speakers.edit_view', event_id=event.id, speaker_id=speaker.id)
            rv = self.app.post(url, data=dict(
                name='name2',
                email='email2@gmail.com',
                organisation="FOSSASIA2",
                country="India2"
            ), follow_redirects=True)

            self.assertTrue("Speaker has been saved" in rv.data, msg=rv.data)
            url = url_for('event_speakers.edit_view', event_id=event.id, speaker_id=speaker.id)
            rv = self.app.get(url, follow_redirects=True)
            self.assertTrue("name2" in rv.data, msg=rv.data)

    def test_wrong_form_config(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            speaker = ObjectMother.get_speaker()
            speaker.event_id = event.id
            save_to_db(speaker, "Speaker saved")
            url = url_for('event_speakers.edit_view', event_id=event.id, speaker_id=speaker.id)
            rv = self.app.get(url, follow_redirects=True)
            self.assertFalse("incorrectly configured" in rv.data, msg=rv.data)

if __name__ == '__main__':
    unittest.main()

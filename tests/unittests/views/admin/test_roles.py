import unittest

from flask import url_for

from app import current_app as app
from app.helpers.data import save_to_db
from app.helpers.data_getter import DataGetter
from app.models.role import Role
from app.models.role_invite import RoleInvite
from app.models.users_events_roles import UsersEventsRoles
from populate_db import populate
from tests.unittests.object_mother import ObjectMother
from tests.unittests.views.view_test_case import OpenEventViewTestCase


class TestRoles(OpenEventViewTestCase):
    def test_role_create_post(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            user = ObjectMother.get_user()
            save_to_db(user, "New user saved")
            populate()
            data = {
                'user_email': user.email,
                'user_role': 'coorganizer'
            }
            rv = self.app.post(url_for('event_roles.create_view', event_id=event.id), follow_redirects=True, data=data)

            # Check if user has been sent a Role Invite
            role = Role.query.filter_by(name='coorganizer').first()
            ri = RoleInvite.query.filter_by(email=user.email, event=event, role=role).first()
            self.assertTrue(ri is not None, msg=rv.data)

    def test_role_delete(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            user = ObjectMother.get_user()
            save_to_db(user, "New user saved")
            populate()
            role = Role.query.filter_by(name='coorganizer').first()
            uer = UsersEventsRoles(user, event, role)
            save_to_db(uer, "UER Saved")
            rv = self.app.get(url_for('event_roles.delete_view', uer_id=uer.id, event_id=event.id),
                              follow_redirects=True)
            uer = UsersEventsRoles.query.get(uer.id)
            self.assertTrue(uer is None, msg=rv.data)

    def test_role_update(self):
        with app.test_request_context():
            event = ObjectMother.get_event()
            save_to_db(event, "Event saved")
            user = ObjectMother.get_user()
            save_to_db(user, "New user saved")
            populate()
            role = Role.query.filter_by(name='coorganizer').first()
            uer = UsersEventsRoles(user, event, role)
            save_to_db(uer, "UER Saved")
            data = {
                'user_email': user.email,
                'user_role': 'track_organizer'
            }
            rv = self.app.post(url_for('event_roles.edit_view', uer_id=uer.id, event_id=event.id), data=data,
                               follow_redirects=True)
            uer = DataGetter.get_user_event_roles_by_role_name(event.id, 'track_organizer').first()
            self.assertTrue(uer is not None, msg=rv.data)


if __name__ == '__main__':
    unittest.main()

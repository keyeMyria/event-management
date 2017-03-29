from datetime import datetime, timedelta

from app.models import db


class RoleInvite(db.Model):
    __tablename__ = 'role_invite'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    event = db.relationship('Event', back_populates='role_invites')

    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
    role = db.relationship("Role")

    hash = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    declined = db.Column(db.Boolean)

    def __init__(self, email, event, role, create_time, declined=False):
        self.email = email
        self.event = event
        self.role = role
        self.create_time = create_time
        self.declined = declined

    def has_expired(self):
        # Check if invitation link has expired (it expires after 24 hours)
        return datetime.now() > self.create_time + timedelta(hours=24)

    def __repr__(self):
        return '<RoleInvite %r:%r:%r>' % (self.email,
                                          self.event,
                                          self.role,)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'Invite for %r:%r:%r' % (self.email,
                                        self.event,
                                        self.role)

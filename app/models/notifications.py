from app.models import db

USER_CHANGE_EMAIL = "User email"
TICKET_PURCHASED = 'Ticket(s) Purchased'
EVENT_ROLE_INVITE = 'Event Role Invitation'
NEW_SESSION = 'New Session Proposal'
EVENT_EXPORT_FAIL = 'Event Export Failed'
EVENT_EXPORTED = 'Event Exported'
SESSION_SCHEDULE = 'Session Schedule Change'
NEXT_EVENT = 'Next Event'
SESSION_ACCEPT_REJECT = 'Session Accept or Reject'
INVITE_PAPERS = 'Invitation For Papers'
AFTER_EVENT = 'After Event'
EVENT_PUBLISH = 'Event Published'
TICKET_PURCHASED_ORGANIZER = 'Ticket(s) Purchased to Organizer'
TICKET_RESEND_ORGANIZER = 'Ticket Resend'


class Notification(db.Model):
    """
    Model for storing user notifications.
    """

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref='notifications')

    title = db.Column(db.String)
    message = db.Column(db.Text)
    action = db.Column(db.String)
    received_at = db.Column(db.DateTime)
    has_read = db.Column(db.Boolean)

    def __init__(self, user, title, message, action, received_at, has_read=False):
        self.user = user
        self.title = title
        self.message = message
        self.action = action
        self.received_at = received_at
        self.has_read = has_read

    def __repr__(self):
        return '<Notif %s:%s>' % (self.user, self.title)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '%r: %r' % (self.user, self.title)

from datetime import datetime

from app.models import db

USER_REGISTER = 'User Registration'
USER_CONFIRM = 'User Confirmation'
USER_CHANGE_EMAIL = "User email"
INVITE_PAPERS = 'Invitation For Papers'
NEXT_EVENT = 'Next Event'
NEW_SESSION = 'New Session Proposal'
PASSWORD_RESET = 'Reset Password'
EVENT_ROLE = 'Event Role Invitation'
SESSION_ACCEPT_REJECT = 'Session Accept or Reject'
SESSION_SCHEDULE = 'Session Schedule Change'
EVENT_PUBLISH = 'Event Published'
AFTER_EVENT = 'After Event'
USER_REGISTER_WITH_PASSWORD = 'User Registration during Payment'
TICKET_PURCHASED = 'Ticket(s) Purchased'
TICKET_PURCHASED_ORGANIZER = 'Ticket(s) Purchased to Organizer'
TICKET_CANCELLED = 'Ticket(s) cancelled'
EVENT_EXPORTED = 'Event Exported'
EVENT_EXPORT_FAIL = 'Event Export Failed'
MAIL_TO_EXPIRED_ORDERS = 'Mail Expired Orders'
MONTHLY_PAYMENT_EMAIL = 'Monthly Payment Email'
MONTHLY_PAYMENT_FOLLOWUP_EMAIL = 'Monthly Payment Follow Up Email'
EVENT_IMPORTED = 'Event Imported'
EVENT_IMPORT_FAIL = 'Event Import Failed'


class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String)
    time = db.Column(db.DateTime)
    action = db.Column(db.String)
    subject = db.Column(db.String)
    message = db.Column(db.String)

    def __init__(self, recipient=None, time=None, action=None, subject=None,
                 message=None):
        self.recipient = recipient
        self.time = time
        if self.time is None:
            self.time = datetime.now()
        self.action = action
        self.subject = subject
        self.message = message

    def __repr__(self):
        return '<Mail %r to %r>' % (self.id, self.recipient)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'Mail %r by %r' % (self.id, self.recipient,)

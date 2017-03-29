from datetime import datetime

from app.models import db

TICKET = 'ticket'
EVENT = 'event'


class AccessCode(db.Model):
    __tablename__ = "access_codes"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    access_url = db.Column(db.String)
    is_active = db.Column(db.Boolean)
    tickets_number = db.Column(db.Integer)  # For event level access this holds the max. uses
    min_quantity = db.Column(db.Integer)
    max_quantity = db.Column(db.Integer)  # For event level access this holds the months for which it is valid
    valid_from = db.Column(db.DateTime, nullable=True)
    valid_till = db.Column(db.DateTime, nullable=True)
    tickets = db.Column(db.String)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    event = db.relationship('Event', backref='access_codes', foreign_keys=[event_id])
    created_at = db.Column(db.DateTime)
    marketer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    marketer = db.relationship('User', backref='access_codes')

    used_for = db.Column(db.String)

    def __init__(self,
                 code=None,
                 access_url=None,
                 tickets_number=None,
                 min_quantity=None,
                 max_quantity=None,
                 valid_from=None,
                 valid_till=None,
                 is_active=True,
                 used_for=None,
                 event_id=None):
        self.code = code
        self.access_url = access_url
        self.tickets_number = tickets_number
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.valid_from = valid_from
        self.valid_till = valid_till
        self.event_id = event_id
        self.is_active = is_active
        self.created_at = datetime.utcnow()
        self.used_for = used_for
    def __repr__(self):
        return '<AccessCode %r>' % self.id

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.code
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {'id': self.id,
                'code': self.code,
                'access_url': access_url,
                'tickets_number': self.tickets_number,
                'min_quantity': self.min_quantity,
                'max_quantity': self.max_quantity,
                'used_for': self.used_for,
                'valid_from': self.valid_from,
                'valid_till': self.valid_till,
                'event_id': self.event_id,
                'is_active': self.is_active}

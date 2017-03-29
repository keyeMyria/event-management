from sqlalchemy.orm import backref

from app.models import db


class EventCopyright(db.Model):
    """
    Copyright Information about an event.
    """
    __tablename__ = 'event_copyright'

    id = db.Column(db.Integer, primary_key=True)
    holder = db.Column(db.String)
    holder_url = db.Column(db.String)
    licence = db.Column(db.String)
    licence_url = db.Column(db.String)
    year = db.Column(db.Integer)
    logo = db.Column(db.String)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    event = db.relationship('Event', backref=backref('copyright', uselist=False))

    def __init__(self,
                 holder=None,
                 holder_url=None,
                 licence=None,
                 licence_url=None,
                 year=None,
                 logo=None,
                 event=None):
        self.holder = holder
        self.holder_url = holder_url
        self.licence = licence
        self.licence_url = licence_url
        self.year = year
        self.logo = logo
        self.event = event

    def __repr__(self):
        return '<Copyright %r>' % self.holder

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.holder

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'holder': self.holder,
            'holder_url': self.holder_url,
            'licence': self.licence,
            'licence_url': self.licence_url,
            'year': self.year,
            'logo': self.logo
        }

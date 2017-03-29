from datetime import datetime

from sqlalchemy.orm import backref

from app.models import db


class ExportJob(db.Model):
    """Export Jobs model class"""
    __tablename__ = 'export_jobs'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)

    user_email = db.Column(db.String)
    # not linking to User because when user is deleted, this will be lost

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    event = db.relationship('Event', backref=backref('export_jobs'))

    def __init__(self, task=None, user_email=None, event=None):
        self.task = task
        self.user_email = user_email
        self.event = event
        self.start_time = datetime.now()

    def __repr__(self):
        return '<ExportJob %d for event %d>' % (self.id, self.event.id)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.__repr__()

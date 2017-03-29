import datetime

from app.helpers.date_formatter import DateFormatter
from app.helpers.versioning import clean_up_string, clean_html
from app.models import db

speakers_sessions = db.Table('speakers_sessions', db.Column(
    'speaker_id', db.Integer, db.ForeignKey('speaker.id', ondelete='CASCADE')), db.Column(
    'session_id', db.Integer, db.ForeignKey('session.id', ondelete='CASCADE')))


class Session(db.Model):
    """Session model class"""
    __tablename__ = 'session'
    __versioned__ = {
        'exclude': []
    }
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String)
    short_abstract = db.Column(db.Text)
    long_abstract = db.Column(db.Text)
    comments = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id', ondelete='CASCADE'))
    speakers = db.relationship(
        'Speaker',
        secondary=speakers_sessions,
        backref=db.backref('sessions', lazy='dynamic'))
    language = db.Column(db.String)
    microlocation_id = db.Column(db.Integer, db.ForeignKey('microlocation.id', ondelete='CASCADE'))
    session_type_id = db.Column(db.Integer, db.ForeignKey('session_type.id', ondelete='CASCADE'))
    level = db.Column(db.String)

    slides = db.Column(db.String)
    video = db.Column(db.String)
    audio = db.Column(db.String)
    signup_url = db.Column(db.String)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'))
    state = db.Column(db.String, default="pending")
    in_trash = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    trash_date = db.Column(db.DateTime)
    submission_date = db.Column(db.DateTime)
    submission_modifier = db.Column(db.String)
    state_email_sent = db.Column(db.Boolean, default=False)

    def __init__(self,
                 title=None,
                 subtitle=None,
                 short_abstract='',
                 long_abstract='',
                 comments=None,
                 start_time=None,
                 end_time=None,
                 track=None,
                 language=None,
                 microlocation=None,
                 speakers=None,
                 event_id=None,
                 state="pending",
                 slides=None,
                 video=None,
                 audio=None,
                 signup_url=None,
                 session_type=None,
                 level=None,
                 created_at=None,
                 state_email_sent=False,
                 in_trash=False,
                 trash_date=None):

        if speakers is None:
            speakers = []

        self.title = title
        self.subtitle = subtitle
        self.short_abstract = short_abstract
        self.long_abstract = long_abstract
        self.comments = comments
        self.start_time = start_time
        self.end_time = end_time
        self.track = track
        self.language = language
        self.microlocation = microlocation
        self.speakers = speakers
        self.event_id = event_id
        self.state = state
        self.slides = slides
        self.video = video
        self.audio = audio
        self.signup_url = signup_url
        self.session_type = session_type
        self.level = level
        self.created_at = created_at
        self.in_trash = in_trash
        self.trash_date = trash_date
        self.state_email_sent = state_email_sent

    @staticmethod
    def get_service_name():
        return 'session'

    @property
    def is_accepted(self):
        return self.state == "accepted"

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'short_abstract': self.short_abstract,
            'long_abstract': self.long_abstract,
            'comments': self.comments,
            'begin': DateFormatter().format_date(self.start_time),
            'end': DateFormatter().format_date(self.end_time),
            'track': self.track.id if self.track else None,
            'speakers': [
                {'id': speaker.id,
                 'name': speaker.name} for speaker in self.speakers
                ],
            'level': self.level,
            'microlocation': self.microlocation.id
            if self.microlocation else None
        }

    def __repr__(self):
        return '<Session %r>' % self.title

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __setattr__(self, name, value):
        if name == 'short_abstract' or name == 'long_abstract' or name == 'comments':
            super(Session, self).__setattr__(name, clean_html(clean_up_string(value)))
        else:
            super(Session, self).__setattr__(name, value)

    def __unicode__(self):
        return self.title

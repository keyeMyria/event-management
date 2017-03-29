from app.models import db


class CustomPlaceholder(db.Model):
    """email notifications model class"""
    __tablename__ = 'custom_placeholder'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    thumbnail = db.Column(db.String)
    copyright = db.Column(db.String)
    origin = db.Column(db.String)

    def __init__(self,
                 name=None,
                 url=None,
                 thumbnail=None,
                 copyright=None,
                 origin=None):
        self.name = name
        self.url = url
        self.thumbnail = thumbnail
        self.copyright = copyright
        self.origin = origin

    def __str__(self):
        return 'Name:' + unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return unicode(self.id)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'thumbnail': self.thumbnail,
            'copyright': self.copyright,
            'origin': self.origin
        }

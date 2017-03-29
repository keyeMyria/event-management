from app.models import db


class ImageConfig(db.Model):
    """image config model class"""
    __tablename__ = 'image_config'
    id = db.Column(db.Integer,
                   primary_key=True)
    page = db.Column(db.String)
    size = db.Column(db.String)

    def __init__(self,
                 page=None,
                 size=None):
        self.page = page
        self.size = size

    def __str__(self):
        return 'Page:' + unicode(self.page).encode('utf-8')

    def __unicode__(self):
        return unicode(self.id)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'page': self.page,
            'size': self.size
        }

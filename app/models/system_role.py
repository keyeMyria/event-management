from app.models import db

from app.models.panel_permissions import PanelPermission


class CustomSysRole(db.Model):
    """Custom System Role
    """
    __tablename__ = 'custom_sys_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def can_access(self, panel_name):
        perm = PanelPermission.query.filter_by(role=self,
                                               panel_name=panel_name).first()
        if perm:
            return perm.can_access
        else:
            return False

    def __repr__(self):
        return '<CustomSysRole %r>' % self.name

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name


class UserSystemRole(db.Model):
    """User Custom System Role
    """
    __tablename__ = 'user_system_role'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref='sys_roles')

    role_id = db.Column(db.Integer, db.ForeignKey('custom_sys_role.id', ondelete='CASCADE'))
    role = db.relationship('CustomSysRole')

    def __init__(self, user, role):
        self.user = user
        self.role = role

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '%r as %r' % (self.user, self.role)

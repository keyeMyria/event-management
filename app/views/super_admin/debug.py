import json
import os
from datetime import datetime, timedelta

import flask_login
from flask import Blueprint
from flask import render_template
from flask import request, current_app

from app.helpers.flask_ext.helpers import get_real_ip
from app.views.super_admin import check_accessible, list_navbar, BASE

sadmin_debug = Blueprint('sadmin_debug', __name__, url_prefix='/admin/debug')


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, timedelta):
        return obj.microseconds

    return '<Object ' + type(obj).__name__ + '>'


@sadmin_debug.before_request
def verify_accessible():
    return check_accessible(BASE)


@sadmin_debug.route('/')
@flask_login.login_required
def display_debug_info():
    return render_template('gentelella/super_admin/debug/debug.html',
                           ip=get_real_ip(),
                           cookies=request.cookies,
                           config=json.dumps(dict(current_app.config), sort_keys=True, indent=4, default=json_serial),
                           environment=json.dumps(dict(os.environ.data), sort_keys=True, indent=4, default=json_serial),
                           navigation_bar=list_navbar(),
                           headers=request.headers)

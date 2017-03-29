from urllib2 import urlopen

from flask import request
from flask.json import JSONEncoder
from jinja2 import Undefined
from slugify import SLUG_OK
from slugify import slugify as unicode_slugify


def get_real_ip(local_correct=False):
    try:
        if 'X-Forwarded-For' in request.headers:
            ip = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
        else:
            ip = request.remote_addr or None

        if local_correct and (ip == '127.0.0.1' or ip == '0.0.0.0'):
            ip = urlopen('http://ip.42.pl/raw').read()  # On local test environments
    except:
        ip = None

    return ip


class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'


class SilentUndefined(Undefined):
    """
    From http://stackoverflow.com/questions/6190348/
    Don't break page loads because vars aren't there!
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        return False

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
        __float__ = __complex__ = __pow__ = __rpow__ = \
        _fail_with_undefined_error


def slugify(text):
    """Generates an ASCII-only slug."""
    return unicode(unicode_slugify(text, ok=SLUG_OK + ',').replace(',', '--'))


def deslugify(text):
    return text.replace('--', ',').replace('-', " ")


def camel_case(text):
    text = slugify(text).replace('-', " ")
    return ''.join(x for x in text.title() if not x.isspace())

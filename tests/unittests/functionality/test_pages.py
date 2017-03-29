# -*- coding: utf-8 -*-
import unittest

from flask import request
from jinja2 import TemplateNotFound

from app import current_app as app
from tests.unittests.setup_database import Setup
from tests.unittests.utils import OpenEventTestCase


class TestPagesUrls(OpenEventTestCase):
    def setUp(self):
        self.app = Setup.create_app()

    def test_event_name(self):
        """Tests all urls with GET method"""
        with app.test_request_context():

            for rule in app.url_map.iter_rules():
                methods = ','.join(rule.methods)
                if "<" not in str(rule) and \
                        "favicon" not in str(rule) and \
                        "check_email" not in str(rule) and \
                        "set_role" not in str(rule) and \
                        "GET" in methods:
                    try:
                        response = self.app.get(request.url[:-1] + str(rule).replace('//', '/'),
                                                follow_redirects=True)

                        if 'api' in str(rule):
                            self.assertTrue(response.status_code in [200, 302, 401, 404], msg=response.data)
                        else:
                            self.assertTrue(response.status_code in [200, 302, 401], msg=response.data)
                    except TemplateNotFound:
                        pass
                    except AttributeError:
                        pass
                    except ValueError:
                        pass


if __name__ == '__main__':
    unittest.main()

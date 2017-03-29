import json
import os
import shutil
import time
import unittest

from app import current_app as app
from test_export_import import ImportExportBase
from tests.unittests.api.utils import create_event, get_path, create_services
from tests.unittests.auth_helper import register
from tests.unittests.setup_database import Setup


class TestImportUploads(ImportExportBase):
    """
    Test Import for media uploads
    """

    def setUp(self):
        self.app = Setup.create_app()
        with app.test_request_context():
            register(self.app, u'test@example.com', u'test')
            create_event(creator_email='test@example.com')
            create_services(1, '1')

    def _update_json(self, file, field, value, number=None):
        fp = 'static/uploads/test_event_import/%s' % file
        ptr = open(fp)
        data = json.loads(ptr.read())
        if file == 'event':
            data[field] = value
        else:
            data[number - 1][field] = value
        ptr.close()
        ptr = open(fp, 'w')
        ptr.write(json.dumps(data, indent=4))
        ptr.close()

    def _create_file(self, name):
        f = open('static/uploads/test_event_import/%s' % name, 'w+')
        f.write('test')
        f.close()

    def _get_event_value(self, path, field):
        resp = self.app.get(path)
        self.assertEqual(resp.status_code, 200, resp.data)
        data = json.loads(resp.data)
        return data[field]

    def _make_zip_from_dir(self):
        dir_path = 'static/uploads/test_event_import'
        shutil.make_archive(dir_path, 'zip', dir_path)
        file = open(dir_path + '.zip', 'r').read()
        os.remove(dir_path + '.zip')
        return file

    def _do_succesful_import(self, file):
        upload_path = get_path('import', 'json')
        resp = self._upload(file, upload_path, 'event.zip')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('task_url', resp.data)
        task_url = json.loads(resp.data)['task_url']
        # wait for done
        while True:
            resp = self.app.get(task_url)
            if 'SUCCESS' in resp.data:
                self.assertIn('result', resp.data)
                dic = json.loads(resp.data)['result']
                break
            if resp.status_code != 200:
                dic = json.loads(resp.data)
                break
            time.sleep(2)
        return dic

    def test_media_successful_uploads(self):
        """
        Test successful uploads of relative and direct links,
        both types of media
        """
        self._create_set()
        self._update_json('event', 'background_image', '/bg.png')
        self._create_file('bg.png')
        self._update_json('speakers', 'photo', '/spkr.png', 1)
        self._create_file('spkr.png')
        self._update_json('sponsors', 'logo', 'http://google.com/favicon.ico', 1)
        # import
        data = self._make_zip_from_dir()
        event_dic = self._do_succesful_import(data)
        # checks
        resp = self.app.get(event_dic['background_image'])
        self.assertEqual(resp.status_code, 200)
        # speaker
        photo = self._get_event_value(
            get_path(2, 'speakers', 2), 'photo'
        )
        resp = self.app.get(photo)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('http://', photo)
        # sponsor
        logo = self._get_event_value(
            get_path(2, 'sponsors', 2), 'logo'
        )
        self.assertIn('sponsors', logo)
        self.assertNotEqual(logo, 'http://google.com/favicon.ico')
        resp = self.app.get(logo)
        self.assertEqual(resp.status_code, 200)

    def test_non_existant_media_import(self):
        """
        Tests when relative link to a media if non-existant
        """
        self._create_set()
        self._update_json('event', 'background_image', '/non.png')
        # import
        data = self._make_zip_from_dir()
        event_dic = self._do_succesful_import(data)
        # check
        self.assertEqual(event_dic['background_image'], None)

    def test_version_preserved(self):
        """
        Tests if version data is being preserved
        """
        self._create_set()
        data_old = json.loads(open('static/uploads/test_event_import/event').read())
        # import
        data = self._make_zip_from_dir()
        event_dic = self._do_succesful_import(data)
        for i in data_old['version']:
            self.assertEqual(
                data_old['version'][i], event_dic['version'][i],
                json.dumps(data_old['version']) + json.dumps(event_dic['version'])
            )


if __name__ == '__main__':
    unittest.main()

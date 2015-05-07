__author__ = 'szeitlin'

from app import app
import app as appmod

import unittest
from flask.ext.testing import TestCase

try:
    print(app.create_index.__doc__)
except Exception as e:
    print(e)

class FlaskTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        #create a test app that every test case can use

        self.test_app = app.test_client()

    def test_connection(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertEqual(response.status_code, 200)

    def test_no_connection(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertIn('ConnectionError', response)

    def test_database_already_exists(self):
        tester = app.create_index(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertIn('IndexAlreadyExistsException', response)

    def test_mapping_does_not_exist(self):
        tester = app.get_mapping(self)
        response = tester.get('/', content_type=('html/text'))
        #self.as

    def test_mapping_exists(self):
        tester = app.get_mapping(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertIn('mappings', response)

    def test_put_mapping(self):
        tester = app.put_mapping(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertIsNone(response)

    def test_put_mapping_fails(self):
        tester = app.put_mapping(self)
        response = tester.get('/', content_type=('html/text'))
        #self.

if __name__ == '__main__':
    unittest.main()



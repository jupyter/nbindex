__author__ = 'szeitlin'

from api import app
import api

import unittest
from flask import Flask, jsonify
from flask.ext.testing import TestCase
from flask_restful import Api, Resource

#this just tests if the test suite is finding the flask app file

try:
    print(api.IndexAPI.put.__doc__)
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
        app.config['TESTING'] = True
        self.api = app.test_client()

    def test_connection(self):
        tester = api.test_client(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertEqual(response.status_code, 200)

    def test_no_connection(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type=('html/text'))
        self.assertIn('ConnectionError', response)

    def test_database_already_exists(self):
        tester = api.IndexAPI.put(Resource, 'test') #fix this later
        response = tester.get('/', content_type=('html/text'))
        self.assertIn('IndexAlreadyExistsException', response)

    def test_mapping_does_not_exist(self):
        tester = api.MappingAPI.get(self, 'nannoo', 'nanana')
        response = tester.get('/', content_type=('html/text'))
        #self.as

    def test_mapping_exists(self):
        tester = api.MappingAPI.get(self, 'test', 'notebook')
        response = tester.get('/', content_type=('html/text'))
        self.assertIn('mappings', response)

    def test_put_mapping(self):
        tester = api.MappingAPI.put(self, 'blah', 'notebook')
        response = tester.get('/', content_type=('html/text'))
        self.assertIsNone(response)

    def test_put_mapping_fails(self):
        tester = api.MappingAPI.put(self, 'test', 'notebook')
        response = tester.get('/', content_type=('html/text'))
        #self.

if __name__ == '__main__':
    unittest.main()



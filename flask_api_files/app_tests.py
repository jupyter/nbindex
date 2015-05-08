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
        tester = app.test_client()
        response = tester.get('/data/', content_type=('html/text'))
        self.assertEqual(response.status_code, 200)

    def test_no_connection(self):
        tester = app.test_client(self)
        response = tester.get('/data/', content_type=('html/text'))
        self.assertIn('ConnectionError', response.status)

    def test_index_does_not_exist(self):
        tester = api.MappingAPI.get('nannoo', 'nanana')
        response = tester.get('/mappings', content_type=('html/text'))
        self.assertIn('IndexMissingException', response.status[1])

    def test_index_already_exists(self):
        tester = api.IndexAPI.put('test')
        response = tester.get('/data/', content_type=('html/text'))
        print(response.status)
        #self.assertIn('IndexAlreadyExistsException', response.status)

    def test_mapping_does_not_exist(self):
        tester = api.MappingAPI.get('test', 'nanana')
        response = tester.get('/mappings/', content_type=('html/text'))
        #self.as

    def test_mapping_exists(self):
        tester = api.MappingAPI.get('test', 'notebook')
        response = tester.get('/mappings/', content_type=('html/text'))
        self.assertIn('mappings', response.status)

    def test_put_mapping(self):
        tester = api.MappingAPI.put('blah', 'notebook')
        response = tester.get('/mappings/', content_type=('html/text'))
        self.assertIsNone(response.status)

    def test_put_mapping_fails(self):
        tester = api.MappingAPI.put('test', 'notebook')
        response = tester.get('/mappings/', content_type=('html/text'))
        print(response.status)
        #self.assertIn('IndexMissing')

if __name__ == '__main__':
    unittest.main()



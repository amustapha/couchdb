import unittest
from unittest import TestCase
from unittest.mock import Mock, patch

from couchdb.doc import CouchDB


class BaseTestCase(TestCase):
    def setUp(self):
        self.couch = CouchDB('https://localhost:5984', 'me', 'fake-pass')

        self.request_get = Mock()
        self.request_get.return_value.json.return_value = {'_id': 'fake-id', 'name': 'Abdulhakeem'}

        self.request_post = Mock()
        self.request_post.return_value.json.return_value = {'ok': True}

        self.request_put = Mock()
        self.request_put.return_value.json.return_value = {'ok': True}

        patch.multiple('couchdb.doc.requests',
                       get=self.request_get,
                       post=self.request_post,
                       put=self.request_put).start()

        self.addCleanup(patch.stopall)


class TestCouchDB(BaseTestCase):

    def test_connect(self):
        self.request_get.return_value.json.return_value = ['db_1', 'db_2']
        expected = ['db_1', 'db_2']
        result = self.couch.get_databases()
        self.assertListEqual(expected, result)

    def test_create_db(self):
        result = self.couch.create('database')
        expected = 'database'
        self.assertEqual(expected, result.name)

    def test_use_db(self):
        result = self.couch.use('database')
        expected = 'database'
        self.assertEqual(expected, result.name)


class TestDatabase(BaseTestCase):
    
    def setUp(self):
        super(TestDatabase, self).setUp()
        self.db = self.couch.use('database')

    def test_create_doc_without_id(self):
        self.db.create(name='Abdulhakeem')
        assert self.request_post.called

    def test_create_doc_with_id(self):
        self.db.create(name='Abdulhakeem', _id='fake-id')
        assert self.request_put.called


if __name__ == '__main__':
    unittest.main()

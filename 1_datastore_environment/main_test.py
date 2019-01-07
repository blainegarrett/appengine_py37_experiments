import unittest
import main
import urllib
import os
from google.cloud import datastore


class DatastoreEnvironmentTests(unittest.TestCase):
    def test_datastore_healthcheck(self):
        """
        Ensure that the test datastore is up and running
        """

        datastore_client_host = 'http://%s' % os.environ['DATASTORE_EMULATOR_HOST']

        with urllib.request.urlopen(datastore_client_host) as response:
            html = response.read()
            assert(b'Ok' in html)

    def test_query(self):
        """
        Ensure we can create an instance of the datastore and query
        """
        datastore_client = datastore.Client()
        self.assertIsInstance(list(datastore_client.query().fetch(1)), list)


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Client
        # Reset Datastore
        super(IntegrationTests, cls).setUpClass()

        main.app.testing = True
        cls.client = main.app.test_client()
        cls.ds_client = datastore.Client()

    def setUp(self):
        """
        Delete test data
        """

        super(IntegrationTests, self).setUp()
        query = self.ds_client.query()
        query.keys_only()

        keys = list([e.key for e in query.fetch(limit=100)])

        self.ds_client.delete_multi(keys)

    def test_index(self):
        """
        Test the hello world route handler
        """
        r = self.client.get('/')
        self.assertEquals(200, r.status_code)
        self.assertTrue('Hello World' in r.data.decode('utf-8'))

    def test_upsert(self):
        """
        Test that our upsert route handler inserts data
        """
        # Set Up Test Data
        keys = [
            self.ds_client.key('Task', 'test1'),
            self.ds_client.key('Task', 'test2')
        ]

        # Test Before State (empty)
        tasks = self.ds_client.get_multi(keys)
        self.assertEquals(0, len(tasks))

        # Test Handler to ensure it created the two above entities
        r = self.client.get('/upsert')
        self.assertEquals(200, r.status_code)
        self.assertTrue('Created 2 Tasks' in r.data.decode('utf-8'))

        # After State (2 new tasks)
        tasks = self.ds_client.get_multi(keys)
        self.assertEquals(2, len(tasks))

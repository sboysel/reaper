import json
import os
import pickle
import unittest

import psycopg2
from lib import database


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        path = (
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.pardir
                    )
                ),
                'config.json'
            )
        )
        settings = None
        with open(path, 'r') as file_:
            settings = json.load(file_)['options']['datasource']

        self.database = database.Database(settings)

    def test_pickling(self):
        # Arrange
        self.database.connect()

        # Act
        pickled = pickle.dumps(self.database)
        unpickled = pickle.loads(pickled)

        # Assert
        self.assertIsInstance(unpickled, database.Database)
        self.assertIsInstance(
            unpickled._connection, psycopg2.extensions.connection
        )
        self.assertTrue(unpickled._connected)

    def test_connect(self):
        # Act
        self.database.connect()

        # Assert
        self.assertTrue(self.database._connected)

    def test_close(self):
        # Act
        self.database.connect()
        self.database.close()

        # Assert
        self.assertFalse(self.database._connected)

    def test_get_empty(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id = 000000000'

        # Act
        self.database.connect()
        actual = self.database.get(query)

        # Assert
        self.assertIsNone(actual)

    def test_get_single(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id = 1'
        expected = (1, 'ruote-kit')

        # Act
        self.database.connect()
        actual = self.database.get(query)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_multiple(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id IN (1,2)'
        expected = [(1, 'ruote-kit'), (2, 'ruote-kit')]

        # Act
        self.database.connect()
        actual = self.database.get(query)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_post(self):
        # Arrange
        tname = 'foo'
        query = 'CREATE TABLE IF NOT EXISTS {0} (bar INT)'.format(tname)
        expected = tname

        # Act
        self.database.connect()
        self.database.post(query)
        actual = self.database.get('SELECT \'{0}\' FROM information_schema.tables \
                                   WHERE table_schema = \'public\''.format(tname))
        # Assert
        try:
            self.assertCountEqual(expected, actual[0][0])
        finally:
            with self.database.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS {0}'.format(tname))

    def tearDown(self):
        if self.database:
            self.database.close()

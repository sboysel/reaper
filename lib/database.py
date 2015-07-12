import contextlib
import sys

import mysql.connector


class DatabaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Database(object):
    def __init__(self, settings):
        self.settings = settings
        self.settings['autocommit'] = True
        self._connection = None

    def connect(self):
        try:
            self._connection = mysql.connector.connect(**self.settings)
            self._connection.connect()
        except mysql.connector.Error as e:
            msg = 'Failure in connecting to database. Error: {0}'.format(e)
            raise DatabaseError(msg)

    def disconnect(self):
        try:
            if self._connection and self._connection.is_connected():
                self._connection.disconnect()
        except mysql.connector.Error as e:
            msg = 'Failure in disconnecting from database. Error: {0}'.format(
                e
            )
            raise DatabaseError(msg)

    def get(self, query):
        try:
            rows = list()
            with self.cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    rows.append(row)
            
            if len(rows) == 1:
                rows = rows[0]

            return rows
        except mysql.connector.Error as e:
            msg = 'Failure in executing query {0}. Error: {1}'.format(query, e)
            raise DatabaseError(msg)

    def post(self, query):
        try:
            with self.cursor() as cursor:
                cursor.execute(query)
        except mysql.connector.Error as e:
            msg = 'Failure in executing query {0}. Error: {1}'.format(query, e)
            raise DatabaseError(msg)
        finally:
            if cursor:
                cursor.close()

    @contextlib.contextmanager
    def cursor(self):
        if self._connection and self._connection.is_connected():
            cursor = self._connection.cursor()
            try:
                yield cursor
            except:
                raise
            finally:
                cursor.close()
        else:
            raise DatabaseError('No connection to the database.')
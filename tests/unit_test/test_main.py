import os
import unittest

from attributes.unit_test import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    def test_main(self):
        # Test: Project using Mocha
        (result, value) = main.run(
            0, os.path.join(REPOS_PATH, 'superagent'), MockCursor()
        )
        self.assertTrue(result)
        self.assertLess(0, value)

        # Test: Project with no unit tests (when these tests were written)
        (result, value) = main.run(
            0, os.path.join(REPOS_PATH, 'javascript'), MockCursor()
        )
        self.assertFalse(result)
        self.assertEqual(-1, value)


class MockCursor(object):
    def __init__(self):
        super(MockCursor, self).__init__()
        self.record = None

    def execute(self, string):
        pass

    def fetchone(self):
        return ['JavaScript']

    def close(self):
        pass
import unittest

from api import app


class PolicyAggregationTest(unittest.TestCase):
    def setUp(self):
        self.flask_app = app

    def test_app_health(self):
        response = self.flask_app.health()
        self.assertEqual(response, "HEALTHY")

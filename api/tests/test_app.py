import unittest

from api import app


class PolicyAggregationTest(unittest.TestCase):
    TEST_RESPONSES = [
        {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
        {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
        {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
    ]

    def setUp(self):
        self.flask_app = app

    def test_invalid_member_id(self):
        response = self.flask_app.fetch_polices(1)
        self.assertEqual(response, "")

        response = self.flask_app.fetch_polices('invalid_member_number')
        self.assertEqual(response, ("Invalid member_id", 400))

    def test_app_health(self):
        response = self.flask_app.health()
        self.assertEqual(response, "HEALTHY")

import unittest
from unittest.mock import patch

from api import app


class PolicyAggregationTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.test_client = app.app.test_client

        # patch and setup mock return values
        # These need to be patched relative to the app module since that's where
        # they are all called from
        fetch_mock = patch('api.app.fetch')
        self.mock_fetch = fetch_mock.start()
        self.mock_fetch.member_policy_limits.return_value = [
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
            {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
        ]

        policy_mock = patch('api.app.policy')
        self.policy_mock = policy_mock.start()
        self.policy_mock.coalesce_limits.return_value = {}

        self.addCleanup(fetch_mock.stop)
        self.addCleanup(policy_mock.stop)

    def test_health_check(self):
        with self.test_client() as c:
            r = c.get("/health")
            self.assertEqual("HEALTHY", r.data.decode())

    def test_invalid_member_id(self):
        with self.test_client() as c:
            r = c.post("/api/fetch-polices/bad-string")
            self.assertEqual(404, r.status_code)

        with self.test_client() as c:
            r = c.post("/api/fetch-polices/1")
            self.assertEqual(200, r.status_code)

    def test_default_strategy_selection(self):
        strategy_mock = self.policy_mock.CoalesceStrategy
        with self.test_client() as c:
            r = c.post("/api/fetch-polices/1")

            self.assertTrue(strategy_mock.default.called)
            self.assertFalse(strategy_mock.parse_strategy_object.called)

    def test_custom_strategy_selection(self):
        strategy_mock = self.policy_mock.CoalesceStrategy
        with self.test_client() as c:
            r = c.post("/api/fetch-polices/1",
                       data='{"request": "body"}',
                       content_type='application/json')

            self.assertTrue(strategy_mock.parse_strategy_object.called)
            self.assertFalse(strategy_mock.default.called)

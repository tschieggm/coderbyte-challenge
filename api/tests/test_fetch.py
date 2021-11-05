import unittest
from copy import deepcopy
from unittest import mock
from unittest.mock import MagicMock

from api import fetch

TEST_POLICY_APIS = (
    'https://api1.com',
    'https://api2.com',
    'https://api3.com',
)


class FetchMemberPolicyLimitsTest(unittest.TestCase):
    def setUp(self):
        self.api_domains = list(deepcopy(TEST_POLICY_APIS))
        self.member_number = 123

    @mock.patch('requests.get')
    def test_api_fetch(self, mock_get):
        fetch.member_policy_limits(self.member_number, self.api_domains)
        self.assertEqual(3, mock_get.call_count)

        call_args = [c.args[0] for c in mock_get.call_args_list]
        self.assertEqual([
            'https://api1.com?member_id=123',
            'https://api2.com?member_id=123',
            'https://api3.com?member_id=123',
        ], call_args)

    @mock.patch('requests.get')
    def test_fetch_results_combined(self, mock_get):
        limit_responses = [
            {'deductible': 500, 'oop_max': 2000, 'stop_loss': 5000},
            {'deductible': 1000, 'oop_max': 4000, 'stop_loss': 10000},
            {'deductible': 1500, 'oop_max': 6000, 'stop_loss': 20000}
        ]

        # mock out the request/response calls
        json_mock = MagicMock()
        json_mock.json.side_effect = limit_responses
        mock_get.return_value = json_mock

        limits = fetch.member_policy_limits(self.member_number,
                                            self.api_domains)

        self.assertEqual(3, mock_get.call_count)
        self.assertEqual(limit_responses, limits)

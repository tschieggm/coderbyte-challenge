import unittest
from copy import deepcopy

from api.policy import CoalesceStrategy, aggregate_single_policy_limit, \
    LimitType, Aggregation, coalesce_limits

DEFAULT_TEST_POLICY_LIMITS = [
    {'deductible': 500, 'oop_max': 2000, 'stop_loss': 5000},
    {'deductible': 1000, 'oop_max': 4000, 'stop_loss': 10000},
    {'deductible': 1500, 'oop_max': 6000, 'stop_loss': 20000},
]

DEFAULT_STRATEGY_OBJ = {
    "deductible": "MIN",
    "oop_max": "AVG",
    "stop_loss": "MAX"
}


class PolicyCoalesceStrategyTests(unittest.TestCase):
    def setUp(self):
        self.strategy_obj = deepcopy(DEFAULT_STRATEGY_OBJ)

    def test_parse_strategy_object(self):
        strategy = CoalesceStrategy.parse_strategy_object(self.strategy_obj)
        self.assertEqual(Aggregation.MIN, strategy[LimitType.DEDUCTIBLE])
        self.assertEqual(Aggregation.AVG, strategy[LimitType.OOP_MAX])
        self.assertEqual(Aggregation.MAX, strategy[LimitType.STOP_LOSS])

    def test_invalid_strategy_object(self):
        with self.assertRaises(ValueError) as context:
            CoalesceStrategy._validate_strategy_obj({
                LimitType.DEDUCTIBLE: Aggregation.MIN,
                LimitType.OOP_MAX: Aggregation.MIN,
            })
        self.assertIn('missing in CoalesceStrategy', str(context.exception))

        with self.assertRaises(ValueError) as context:
            CoalesceStrategy._validate_strategy_obj({
                LimitType.DEDUCTIBLE: "MIN",
            })
        self.assertIn('Invalid Aggregation', str(context.exception))

        with self.assertRaises(ValueError) as context:
            CoalesceStrategy._validate_strategy_obj({
                'deductible': Aggregation.MIN,
            })
        self.assertIn('Invalid LimitType', str(context.exception))

    def test_strategy_object_indexing(self):
        strategy = CoalesceStrategy.parse_strategy_object(self.strategy_obj)
        self.assertEqual(Aggregation.MIN, strategy[LimitType.DEDUCTIBLE])


class LimitTypeAggregationTests(unittest.TestCase):
    def setUp(self):
        self.test_policy_limits = deepcopy(DEFAULT_TEST_POLICY_LIMITS)
        self.default_strategy = CoalesceStrategy.default()

    def test_deductible_min(self):
        aggregated_value = aggregate_single_policy_limit(
            self.test_policy_limits, LimitType.DEDUCTIBLE, Aggregation.MIN)
        self.assertEqual(500, aggregated_value)

    def test_oop_max_max(self):
        aggregated_value = aggregate_single_policy_limit(
            self.test_policy_limits, LimitType.OOP_MAX, Aggregation.MAX)
        self.assertEqual(6000, aggregated_value)

    def test_stop_loss_avg(self):
        aggregated_value = aggregate_single_policy_limit(
            self.test_policy_limits, LimitType.STOP_LOSS, Aggregation.AVG)
        self.assertEqual(11666, aggregated_value)

    def test_integer_average(self):
        self.test_policy_limits[0]['oop_max'] = 1
        aggregated_value = aggregate_single_policy_limit(
            self.test_policy_limits, LimitType.OOP_MAX, Aggregation.AVG)
        self.assertEqual(3333, aggregated_value)


class PolicyCoalesceLimitsTests(unittest.TestCase):
    def setUp(self):
        self.test_policy_limits = deepcopy(DEFAULT_TEST_POLICY_LIMITS)

        strategy_obj = deepcopy(DEFAULT_STRATEGY_OBJ)
        self.strategy = CoalesceStrategy.parse_strategy_object(strategy_obj)

    def test_coalesce_limits(self):
        coalesced_limits = coalesce_limits(self.test_policy_limits,
                                           self.strategy)

        self.assertEqual({
            'deductible': 500,
            'oop_max': 4000,
            'stop_loss': 20000
        }, coalesced_limits)

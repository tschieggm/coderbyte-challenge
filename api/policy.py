
from enum import Enum


class Aggregation(Enum):
    AVG = "AVG"
    MIN = "MIN"
    MAX = "MAX"

    @classmethod
    def from_str(cls, agg):
        return cls[str.upper(agg)]


# this assumes limit types will not change frequently
# the enum value is what the API uses for external object access
class LimitType(Enum):
    DEDUCTIBLE = 'deductible'
    STOP_LOSS = 'stop_loss'
    OOP_MAX = 'oop_max'

    @staticmethod
    def from_str(limit_type):
        return LimitType[str.upper(limit_type)]

    @classmethod
    def values(cls):
        return set(cls.__members__.values())


class CoalesceStrategy(object):
    _strategy_map = {
        LimitType.DEDUCTIBLE: Aggregation.AVG,
        LimitType.STOP_LOSS: Aggregation.AVG,
        LimitType.OOP_MAX: Aggregation.AVG,
    }

    def __init__(self):
        pass

    def __init__(self, strategy_map_obj):
        """
        Takes in an explicitly defined strategy_map_obj and validates it before
         returning the CoalesceStrategy.
        :param strategy_map_obj: A dict of unique LimitTypes:Aggregation
        """
        self._validate_strategy_obj(strategy_map_obj)
        self._strategy_map = strategy_map_obj

    def __getitem__(self, limit_type: LimitType):
        return self._strategy_map[limit_type]

    @staticmethod
    def _validate_strategy_obj(strategy_map_obj):
        # ensure we have no extraneous or invalid keys or values
        for key, value in strategy_map_obj.items():
            if not isinstance(key, LimitType):
                key_err = "Invalid LimitType in CoalesceStrategy strategy_map"
                raise ValueError(key_err)
            if not isinstance(value, Aggregation):
                key_err = "Invalid Aggregation in CoalesceStrategy strategy_map"
                raise ValueError(key_err)

        # find any missing types by doing set subtraction
        missing_types = LimitType.values() - set(strategy_map_obj.keys())
        if len(missing_types) > 0:
            types_err = f"{missing_types}" \
                        f" missing in CoalesceStrategy strategy_map"
            raise ValueError(types_err)

        # No errors raised indicating all values are specified and correct
        return True

    @classmethod
    def parse_strategy_object(cls, strategy_object):
        """ Parse and validate strategy map object from a python dict """
        strategy = {}
        for key, value in strategy_object.items():
            strategy[LimitType.from_str(key)] = Aggregation.from_str(value)
        return cls(strategy)

    @classmethod
    def default(cls):
        """ The default coalesce strategy is to use average for all
        aggregations """
        return cls.__new__(cls)


def aggregate_single_policy_limit(policy_limits: list, limit_type: LimitType,
                                  agg: Aggregation):
    """
    Aggregates the values of a single policy limit type across multiple policies

    :param limit_type: The limit name to aggregate across a list of policies
    :param policy_limits: The collection of policies with distinct limits
    :param agg: The aggregation to apply to the limit_type of each policy

    :return: A single value representing the aggregated limit across all
    policies
    """
    limit_values = [p[limit_type.value] for p in policy_limits]

    if agg == Aggregation.MIN:
        return min(limit_values)
    elif agg == Aggregation.MAX:
        return max(limit_values)
    elif agg == Aggregation.AVG:
        # cast to int for whole dollar values
        return int(sum(limit_values) / len(limit_values))
    else:
        raise ValueError(f"Invalid Aggregation {agg}")


def coalesce_limits(policy_limits: list, strategy: CoalesceStrategy):
    """
    Takes a list of policies for a single member and aggregates each limit type
    based on the provided CoalesceStrategy.

    :param policy_limits: A list of policy limits for a single member
    :param strategy: The well defined CoalesceStrategy for aggregating policy
    limits
    :return: A single coalesced policy with aggregated limits
    """
    coalesced_policy = {}

    # all other limit types will be dropped from supplies policy_limits list
    for limit_type in LimitType:
        aggregation = strategy[limit_type]
        limit_val = aggregate_single_policy_limit(policy_limits, limit_type,
                                                  aggregation)
        coalesced_policy[limit_type.value] = limit_val

    return coalesced_policy

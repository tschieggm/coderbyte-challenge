import urllib.parse

from enum import Enum
from random import randrange


class Aggregation(Enum):
    AVG = "AVG"
    MIN = "MIN"
    MAX = "MAX"


# this assumes limit types will not change frequently
# the enum value is what the API uses for object access
class LimitTypes(Enum):
    DEDUCTIBLE = 'deductible'
    STOP_LOSS = 'stop_loss'
    OOP_MAX = 'oop_max'


class CoalesceStrategy(object):
    _strategy_map = {
        LimitTypes.DEDUCTIBLE: Aggregation.AVG,
        LimitTypes.STOP_LOSS: Aggregation.AVG,
        LimitTypes.OOP_MAX: Aggregation.AVG,
    }

    def __init__(self):
        pass

    def strategy_for(self, limit_type: LimitTypes):
        return self._strategy_map[limit_type]

    @classmethod
    def default(cls):
        """ The default coalesce strategy is to use average for all aggregations """
        return cls()
    #
    # @classmethod
    # def parse_strategy_object(self, strategy_object):
    #     for key, value in strategy_object.items():
    #         if key in self.strategy_map
    #     return cls(data, db_connection)


def fetch_member_limits(member_id, api_domains, coalesce_strategy=None):
    request_args = {'member_id': member_id}
    url_encoded_args = urllib.parse.urlencode(request_args)
    policy_limits = []
    for api_domain in api_domains:
        url = f'{api_domain}?{url_encoded_args}'
        # response = requests.get(url)
        policy_limits.append({
            'deductible': randrange(4000),
            'stop_loss': randrange(10000),
            'oop_max': randrange(5000)
        })

    return policy_limits


def aggregate_single_policy_limit(limit_type: LimitTypes, policy_limits: list, agg: Aggregation):
    """
    Aggregates the values of a single policy limit across multiple policies

    :param limit_type: The limit name to aggregate across a list of policies
    :param policy_limits: The collection of policies with individual limits
    :param agg: The aggregation to apply to the limits

    :return: A single value representing the aggregated limit
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
    coalesced_policy = {}

    # all other limit types will be dropped from supplies policy_limits list
    for limit_type in LimitTypes:
        aggregation = strategy.strategy_for(limit_type)
        limit_val = aggregate_single_policy_limit(limit_type, policy_limits, aggregation)
        coalesced_policy[limit_type.value] = limit_val

    return coalesced_policy

import urllib.parse

import requests as requests


def member_policy_limits(member_id: int, api_domains: list):
    """
    Given a member id - fetch the policy limits from a list of API domains.

    This assumes all APIs are called the same way.

    :param member_id: member we are fetching policy limits for
    :param api_domains: A list of API domains (fully qualified URI strings)
    :return: A collection of policy limit objects - 1 per domain
    """
    request_args = {'member_id': member_id}
    url_encoded_args = urllib.parse.urlencode(request_args)
    policy_limits = []

    for api_domain in api_domains:
        url = f'{api_domain}?{url_encoded_args}'
        # TODO: handle server errors or malformed data
        response = requests.get(url)
        policy_limits.append(response.json())

    return policy_limits

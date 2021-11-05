from flask import Flask

from api import policy
from api import settings

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'coderbyte-challenge server'


@app.route('/health')
def health() -> str:
    return 'HEALTHY'


@app.route('/api/fetch-polices/<int:member_id>', methods=['GET'])
def fetch_polices(member_id: int):
    limits = policy.fetch_member_limits(member_id, settings.POLICY_APIS)

    print(''.join(map(str, limits)))
    coalesce_strategy = policy.CoalesceStrategy.default()
    return policy.coalesce_limits(limits, coalesce_strategy)


@app.route('/api/fetch-polices/<int:member_id>', methods=['POST'])
def fetch_polices_with_strategy(member_id: int):
    limits = policy.fetch_member_limits(member_id, settings.POLICY_APIS)

    print(''.join(map(str, limits)))
    coalesce_strategy = policy.CoalesceStrategy.default()
    return policy.coalesce_limits(limits, coalesce_strategy)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

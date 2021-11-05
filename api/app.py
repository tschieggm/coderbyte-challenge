from flask import Flask, request

from api import policy, fetch, settings

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'coderbyte-challenge server'


@app.route('/health')
def health() -> str:
    return 'HEALTHY'


@app.route('/api/fetch-polices/<int:member_id>', methods=['POST'])
def fetch_polices(member_id: int):
    limits = fetch.member_policy_limits(member_id, settings.POLICY_APIS)

    request_body = request.json
    if request_body:
        strategy = policy.CoalesceStrategy.parse_strategy_object(request_body)
    else:
        strategy = policy.CoalesceStrategy.default()

    return policy.coalesce_limits(limits, strategy)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

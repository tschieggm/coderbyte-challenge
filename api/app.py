import json

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
    all_limits = fetch.member_policy_limits(member_id, settings.POLICY_APIS)

    request_body = request.json
    if request_body:
        # TODO: improve HTTP response codes on validation exceptions
        strategy = policy.CoalesceStrategy.parse_strategy_object(request_body)
    else:
        strategy = policy.CoalesceStrategy.default()

    coalesced_policy_limits = policy.coalesce_limits(all_limits, strategy)

    response = app.response_class(
        response=json.dumps(coalesced_policy_limits),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

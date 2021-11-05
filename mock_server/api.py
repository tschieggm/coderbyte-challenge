import json
import os
from random import randrange

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'coderbyte-challenge mock server'


@app.route('/policies')
def policies():
    member_id = int(request.args.get('member_id'))
    # return mock randomly generated data, use the member_id as a multiplier
    data = {
        'deductible': (randrange(10) * member_id),
        'oop_max': (randrange(1000) * member_id),
        'stop_loss': (randrange(10000) * member_id),
    }

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

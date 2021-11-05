from flask import Flask

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return 'coderbyte-challenge server'


@app.route('/health')
def health() -> str:
    return 'HEALTHY'


@app.route('/api/policy-reconciliation')
def api() -> str:
    return 'HEALTHY'


if __name__ == '__main__':
    app.config.from_object('settings')
    app.run(debug=True, host='0.0.0.0')

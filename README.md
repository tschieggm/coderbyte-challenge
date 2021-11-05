# coderbyte-challenge

Example insurance policy reconciliation API

## Building the API

This project assumes you have docker configured and running in your local environment.

`
docker build -t coderbyte-challenge:latest .
`

## Running the API

`docker run -p 5000:5000 coderbyte-challenge:latest`

## Local Development

Python and pip are required for local development. Using a virtual_env is also typically a good idea.

```
pip install requirements.txt 
python api/app.py
```

### Local Testing

`python -m unittest discover`

## TODO

- Fetch the policy responses in parallel
- Switch to a production read webserver such
  as [Waitress](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/#run-with-a-production-server)
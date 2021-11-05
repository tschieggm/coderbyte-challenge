# coderbyte-challenge

Example insurance policy reconciliation API

## Running the API

This project assumes you have docker and docker compose running in your local
environment.

#### Just the API

`
docker-compose up api
`

#### The API and mock upstream services

`
docker-compose up
`

### Cleaning up

`
docker-compose down --rmi all
`

## Calling the API locally

**Using an average coalesce strategy**

`
curl -X POST http://localhost:5000/api/fetch-polices/1
`

**Using a custom coalesce strategy**

> ```curl -X POST http://localhost:5000/api/fetch-polices/1 -H 'Content-Type: application/json' -d '{"deductible": "MIN", "oop_max": "MIN", "stop_loss": "MIN"}'```

## Local Development

Python and pip are required for local development.

Using a virtual_env is also typically a good idea.

```
pip install -r requirements.txt 
python -m api.app
```

### Local Testing

`python -m unittest discover`

## TODO

- Handling external server errors or malformed data

- Integration tests

- Fetch the policy responses in parallel

- Verify we want averaged policy values in whole dollars

- Utilize Flask app.config to set API urls on build

- Switch to a production read webserver such
  as [Waitress](https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/#run-with-a-production-server)

## Project Instructions

Suppose you have 3 different APIs you can call with member_id as a parameter.

Example API calls would be:

```
https://api1.com?member_id=1
https://api2.com?member_id=1
https://api3.com?member_id=1
```

You'll get responses from these apis with similar responses:

```
API1: {deductible: 1000, stop_loss: 10000, oop_max: 5000}
API2: {deductible: 1200, stop_loss: 13000, oop_max: 6000}
API3: {deductible: 1000, stop_loss: 10000, oop_max: 6000}
```

As you can see above the API's don't always agree. The task is to build an API that calls these APIs
and coalesces the responses with a strategy.

An example strategy could be the average of the response fields. With the average strategy, your
coalesce API would respond with:

`{deductible: 1066, stop_loss: 11000, oop_max: 5666}`

Your API should:

- Take in the member_id as a parameter
- Make the calls to the different APIs
- Coalesce the data returned by the APIs
- As a bonus challenge: allow for the coalescing strategy to be configurable

What we are looking for:

- Testing
- Design Patterns
- Efficiency
- and last but not least creativity!
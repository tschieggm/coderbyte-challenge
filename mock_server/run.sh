#!/bin/bash

set -e

exec python3 flask run --port 5001 &
exec python3 flask run --port 5002 &
exec python3 flask run --port 5003 &

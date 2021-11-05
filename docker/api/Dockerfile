FROM python:3.8-slim-buster

# Copy the requirements.txt first to leverage Docker cache
COPY ./api/requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

# run the tests on build and abort on failure
RUN python -m unittest discover || exit 1

ENTRYPOINT [ "python" ]
CMD [ "-m", "api.app" ]
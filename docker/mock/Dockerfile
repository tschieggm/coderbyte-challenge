FROM python:3.8-slim
ARG FLASK_RUN_PORT
ENV FLASK_RUN_PORT $FLASK_RUN_PORT

# Copy the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT [ "python" ]
CMD [ "-m", "mock_server.api" ]

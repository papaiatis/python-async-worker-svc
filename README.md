# Python Async Worker Service

This is an asynchronous worker service example. It performs basic math. 
It connects to Google PubSub to pull commands to process and publishes the results back to PubSub. 

## Local development
At first, you need to install dependencies and start backend services:
```
make install
make dev-up
```

Then, when all containers are running, run the app:
```
make run
```

## Using with Docker
To build the image:
```
make build
```
To run the image locally:
```
make docker-run
```

## Helper scripts
To publish messages to the input topic, call:
```
make dev-publish <ID> <COMMAND> <ARGS>
```
To listen for result messages, call:
```
make dev-consume
```

## Production
This service needs an input and output PubSub topic and an input subscription to work correctly.
The names of these topics can be configured via environment variables.
Check `settings.py` to see what parameters are available.

For example, to set input and output topic names:
```
WORKER_PUBSUB__INPUT_TOPIC=async-worker-inp
WORKER_PUBSUB__OUTPUT_TOPIC=async-worker-out
```
Subscription names are calculated by postfixing `-sub` to topic names.
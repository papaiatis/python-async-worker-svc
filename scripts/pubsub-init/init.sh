#!/bin/bash

# This script initializes the Pub/Sub emulator. It is run when the pubsub container in the root docker-compose.yml file starts up.
# The examples use the gcloud command line tool to create topics and subscriptions.
# See https://cloud.google.com/sdk/gcloud/ for more information about gcloud commands and flags.
# Note: It is also possible to create topics and subscriptions using the Pub/Sub REST API directly.

echo "Waiting for the Pub/Sub emulator to start..."
while ! curl -s -o /dev/null http://pubsub:8085; do
  sleep 1
done
echo "Pub/Sub emulator started!"

python3 /config/configure.py
import json
import os
import sys

from loguru import logger

os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

from google.cloud import pubsub_v1
from async_worker_svc.settings import get_settings


def convert_to_number(value):
    """Convert a string to an int or float, or leave it as a string if not numeric."""
    try:
        if "." in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return value  # Return as-is if it's not a number


def main():
    # Ensure minimum arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python publish.py <id> <command> [args...]")
        sys.exit(1)

    cmd_id = sys.argv[1]
    command = sys.argv[2]
    args = [convert_to_number(arg) for arg in sys.argv[3:]]  # Collect all remaining arguments as a list

    settings = get_settings()
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.pubsub.project_id, settings.pubsub.input_topic)

    data = {"id": cmd_id, "command": command, "args": args}
    data = json.dumps(data)
    data = data.encode("utf-8")

    logger.info(f"Publishing message {data}")

    response = publisher.publish(topic=topic_path, data=data)
    response.result()


if __name__ == "__main__":
    main()

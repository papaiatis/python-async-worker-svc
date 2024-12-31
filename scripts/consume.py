import os

os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

import json

from google import pubsub_v1
from loguru import logger

from async_worker_svc.settings import get_settings


def main():
    settings = get_settings()
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(settings.pubsub.project_id, settings.pubsub.output_topic + "-sub")

    logger.info(f"Connected to PubSub {publisher.transport._host}")

    while True:
        response = subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 30,
            }
        )
        if response.received_messages:
            logger.info(f"Pulled {len(response.received_messages)} message(s) from PubSub")
        for message in response.received_messages:
            decoded = json.loads(message.message.data.decode())
            logger.info(decoded)
            subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": [message.ack_id],
                }
            )


if __name__ == "__main__":
    main()

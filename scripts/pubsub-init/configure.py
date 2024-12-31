from google import pubsub_v1
from google.api_core.exceptions import AlreadyExists
from loguru import logger

from pydantic import BaseModel


class Subscription(BaseModel):
    topic_path: str
    subscription_path: str


publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

logger.info(f"Connected to PubSub {publisher.transport._host}")

subscriptions: list[Subscription] = [
    Subscription(
        topic_path="projects/local0/topics/async-worker-in",
        subscription_path="projects/local0/subscriptions/async-worker-in-sub",
    ),
    Subscription(
        topic_path="projects/local0/topics/async-worker-out",
        subscription_path="projects/local0/subscriptions/async-worker-out-sub",
    ),
]

for sub in subscriptions:
    try:
        topic = publisher.create_topic(request={"name": sub.topic_path})
        logger.info(f"Topic created {topic.name}")
    except AlreadyExists:
        logger.info(f"The topic '{sub.topic_path}' already exists")

    try:
        sub = subscriber.create_subscription(
            request={
                "name": sub.subscription_path,
                "topic": sub.topic_path,
                "ack_deadline_seconds": 600,
            }
        )
        logger.info(f"Subscription created {sub.name}")
    except AlreadyExists:
        logger.info(f"The subscription '{sub.subscription_path}' already exists")

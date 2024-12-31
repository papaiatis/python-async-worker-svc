import asyncio
import json
import traceback
from json import JSONDecodeError

from google.cloud import pubsub_v1
from google.pubsub_v1 import ReceivedMessage
from loguru import logger
from pydantic import ValidationError

from async_worker_svc.processor import Processor
from async_worker_svc.settings import get_settings
from async_worker_svc.types import OutgoingMessage, IncomingMessage


class PubSubMessageConsumer:
    def __init__(self):
        self._settings = get_settings()
        self._publisher = pubsub_v1.PublisherClient()
        self._subscriber = pubsub_v1.SubscriberClient()
        self._subscription_path = self._subscriber.subscription_path(
            self._settings.pubsub.project_id, self._settings.pubsub.input_topic + "-sub"
        )
        self._output_topic_path = self._publisher.topic_path(
            self._settings.pubsub.project_id, self._settings.pubsub.output_topic
        )
        self._loop = asyncio.get_event_loop()
        self._processor = Processor()

    def _pull_messages(self):
        try:
            logger.info("Waiting for messages to be pulled...")
            response = self._subscriber.pull(
                subscription=self._subscription_path, max_messages=self._settings.pubsub.max_messages
            )
            if response.received_messages:
                logger.success(f"Pulled {len(response.received_messages)} message(s) from PubSub")

            for message in response.received_messages:
                try:
                    decoded = json.loads(message.message.data.decode())
                    msg = IncomingMessage.model_validate(decoded)
                    res = self._processor.process(msg)
                    self._publish_result(res)
                    self._ack(message)
                except (JSONDecodeError, ValidationError):
                    logger.error(f"Invalid message received, skipping...")
                    self._ack(message)
                except Exception as e:
                    logger.exception(f"Unable to process command", ecx_info=e)
                    self._nack(message)
        except Exception as e:
            logger.error(f"Failure processing messages {e}, traceback: {traceback.format_exc()}")
        finally:
            self._loop.call_soon(callback=self._pull_messages)

    def _publish_result(self, result: OutgoingMessage):
        """
        Publishes the result of a command
        """
        logger.success(f"Publishing result for command (#{result.id}): {result.result}")
        data = result.model_dump_json().encode("utf-8")
        self._publisher.publish(topic=self._output_topic_path, data=data)

    def _ack(self, message: ReceivedMessage):
        """
        Acknowledges the message in PubSub
        """
        self._subscriber.acknowledge(
            request={
                "subscription": self._subscription_path,
                "ack_ids": [message.ack_id],
            }
        )

    def _nack(self, message: ReceivedMessage):
        """
        Deliberately refrain from acknowledging the message so it'll be redelivered immediately
        """
        self._subscriber.modify_ack_deadline(
            request={"subscription": self._subscription_path, "ack_ids": [message.ack_id], "ack_deadline_seconds": 0}
        )

    def start(self):
        """
        Starts a forever running loop to pull messages from PubSub
        """
        logger.info("Starting PubSub consumer")
        self._loop.call_soon(callback=self._pull_messages)
        self._loop.run_forever()

    def stop(self):
        """
        Stops pulling messages from PubSub
        """
        logger.info("Stopping PubSub consumer")
        self._loop.stop()

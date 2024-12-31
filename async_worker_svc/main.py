import multiprocessing
import signal
import sys

import flask
from gevent.pywsgi import WSGIServer
from loguru import logger

from async_worker_svc.logger import configure_logger
from async_worker_svc.pubsub import PubSubMessageConsumer
from async_worker_svc.settings import get_settings

app = flask.Flask(__name__)


def sigint_handler(signum, frame):
    # avoids dumping the trace when interrupting the application
    sys.exit(0)


def start_message_processing():
    configure_logger()
    signal.signal(signal.SIGINT, sigint_handler)
    consumer = PubSubMessageConsumer()

    while True:
        try:
            consumer.start()
        except Exception as e:
            logger.exception(f"Error while running the consumer: {e}")
        finally:
            consumer.stop()


@app.route("/health")
def health():
    return flask.jsonify({"status": "OK"})


def main():
    configure_logger()
    signal.signal(signal.SIGINT, sigint_handler)

    worker_proc = multiprocessing.Process(target=start_message_processing, name="worker")
    worker_proc.start()

    settings = get_settings()
    logger.info(f"API is listening on port {settings.port}")
    try:
        server = WSGIServer(("0.0.0.0", settings.port), app, log=None)
        server.serve_forever()
    except Exception as e:
        if worker_proc:
            worker_proc.terminate()
        raise e

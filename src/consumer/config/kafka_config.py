import os

from confluent_kafka import Consumer, Producer

class KafkaConfig:

    def __init__(self, topic=None):
        self._topic = topic or os.getenv("KAFKA_TOPIC_REQUEST", "message-question")
        self._bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

        self._message_consumer = self._create_consumer("message-question-group")
        self._notification_consumer = self._create_consumer("message-notification-group")
        self._message_producer = self._create_producer()

    def _create_consumer(self, groupid):
        try:
            config = {
                "bootstrap.servers": self._bootstrap_servers,
                "group.id": groupid,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
            }
            return Consumer(config)
        except Exception as e:
            raise RuntimeError(f"Failed to create Kafka consumer: {e}")

    def _create_producer(self):
        try:
            config = {
                "bootstrap.servers": self._bootstrap_servers,
            }
            return Producer(config)
        except Exception as e:
            raise RuntimeError(f"Failed to create Kafka producer: {e}")

    @property
    def topic(self):
        return self._topic

    @property
    def message_producer(self):
        return self._message_producer

    @property
    def message_consumer(self):
        return self._message_consumer

    @property
    def notification_consumer(self):
        return self._notification_consumer
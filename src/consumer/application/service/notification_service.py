from confluent_kafka import KafkaException

from src.consumer.config.kafka_config import KafkaConfig

def notification_listener(config: KafkaConfig = KafkaConfig("message-notification")):
    consumer = config.notification_consumer

    consumer.subscribe([config.topic])
    print("Listening for notifications...")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        try:
            print(f"Received notification: {msg.value().decode('utf-8')}")
        except Exception as e:
            print(f"Failed to process notification: {e}")
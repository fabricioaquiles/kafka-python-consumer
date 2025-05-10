import json

from confluent_kafka import KafkaException

from src.consumer.application.dto.message_dto import MessageDto
from src.consumer.application.service.message_processor_service import get_answer
from src.consumer.config.kafka_config import KafkaConfig

def message_listener(config: KafkaConfig = KafkaConfig("message-question")):
    consumer = config.message_consumer
    producer = config.message_producer

    consumer.subscribe([config.topic])
    print("Listening for messages...")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        try:
            message_dto = MessageDto.from_json(json.loads(msg.value().decode("utf-8")))

            headers = dict(msg.headers())

            reply_topic_header = headers.get("kafka_replyTopic")
            correlation_id_header = headers.get("kafka_correlationId")

            if reply_topic_header:
                reply_topic = reply_topic_header.decode("utf-8")
                response = get_answer(message_dto.message)
                producer.produce(
                    reply_topic,
                    value=json.dumps(response),
                    headers=[("kafka_correlationId", correlation_id_header)]
                )
                producer.flush()

        except Exception as e:
            print(f"Failed to process message: {e}")
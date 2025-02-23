"""
Consumes real-time data from Kafka topics and forwards it for processing.

This module uses the kafka-python library to subscribe to one or more Kafka topics.
It includes robust error handling, logging, and a placeholder processing function
for incoming messages. In production, the process_message function should be extended
to integrate with the rest of the data pipeline.

Assumptions:
- Kafka cluster and topics are pre-configured.
- Environment variables or configuration files provide Kafka connection details.
"""

import json
import logging
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError

# Configure logger for this module.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_message(message_value: dict):
    """
    Process a single message.
    
    Args:
        message_value (dict): The JSON-decoded message payload.
    """
    # TODO: Integrate with data cleansing, transformation, and downstream pipelines.
    logger.info(f"Processing message: {message_value}")

def consume_messages(topic: str, bootstrap_servers: list, group_id: str = "fleet-optimization-group"):
    """
    Consume messages from a specified Kafka topic.

    Args:
        topic (str): The Kafka topic to subscribe to.
        bootstrap_servers (list): List of Kafka broker addresses.
        group_id (str): Consumer group ID for coordinated consumption.
    """
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest",
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            consumer_timeout_ms=1000  # Allows the loop to exit gracefully.
        )
        logger.info(f"Subscribed to Kafka topic: {topic}")

        for message in consumer:
            logger.debug(f"Received message at offset {message.offset}")
            try:
                process_message(message.value)
            except Exception as e:
                logger.error(f"Error processing message at offset {message.offset}: {e}")

    except KafkaError as ke:
        logger.error(f"Kafka error encountered: {ke}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")

# Example usage:
if __name__ == "__main__":
    TOPIC = "fleet_data"
    BOOTSTRAP_SERVERS = ["localhost:9092"]
    consume_messages(TOPIC, BOOTSTRAP_SERVERS)

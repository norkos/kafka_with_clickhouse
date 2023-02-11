import logging
from aiokafka import AIOKafkaProducer

from validation_service.utils.logconf import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)


class Kafka:
    instance = None

    def __init__(self, topic: str, connection: str):
        self._topic = topic
        self._connection = connection
        self._producer = self.create_kafka()
        Kafka.instance = self

    def create_kafka(self):
        return AIOKafkaProducer(bootstrap_servers=self._connection)

    async def start(self) -> None:
        await self._producer.start()
        logger.debug('Kafka up')

    async def stop(self) -> None:
        await self._producer.stop()
        logger.debug('Kafka down')

    async def send(self, message: bytes) -> None:
        await self._producer.send_and_wait(self._topic, message)
        logger.debug(f'Sent the event with body={message} to Kafka topic key={self._topic}')

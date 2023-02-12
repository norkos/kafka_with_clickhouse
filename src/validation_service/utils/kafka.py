import asyncio
import json
import logging
from aiokafka import AIOKafkaProducer

from validation_service.event import Event
from validation_service.publisher import AbstractMessageProducer
from validation_service.utils.logconf import DEFAULT_LOGGER
from validation_service.utils.settings import KAFKA_URL, ENCODING, KAFKA_TOPIC

logger = logging.getLogger(DEFAULT_LOGGER)


class KafkaMessageProducer(AbstractMessageProducer):
    instance = None

    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer
        self._topic = KAFKA_TOPIC

    @classmethod
    async def get_instance(cls):
        if not cls.instance:
            producer = AIOKafkaProducer(loop=asyncio.get_event_loop(), bootstrap_servers=KAFKA_URL)
            await producer.start()
            logger.debug('Kafka up')
            cls.instance = cls(producer)
        return cls.instance

    async def stop(self):
        await self._producer.stop()

    async def publish(self, event: Event) -> None:
        try:
            message = json.dumps(event.dict(), default=str).encode(ENCODING)
            await self._producer.send_and_wait(self._topic, message)
            logger.debug(f'Sent the event with body={message} to Kafka topic key={self._topic}')
        except Exception as err:
            logger.error(err)
            raise err

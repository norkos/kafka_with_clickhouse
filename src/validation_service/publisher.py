import json
import logging
from abc import ABC

from validation_service.event import Event
from validation_service.utils.kafka import Kafka
from validation_service.utils.logconf import DEFAULT_LOGGER
from validation_service.utils.settings import ENCODING

logger = logging.getLogger(DEFAULT_LOGGER)


class AbstractMessageProducer(ABC):
    async def publish(self, event: Event) -> None:
        raise NotImplementedError


class KafkaMessageProducer(AbstractMessageProducer):
    producer = None

    def __init__(self):
        self._producer = Kafka.instance

    async def publish(self, event: Event) -> None:
        try:
            message_content = json.dumps(event.dict(), default=str).encode(ENCODING)
            await self._producer.send(message_content)
        except Exception as err:
            logger.error(err)
            raise err

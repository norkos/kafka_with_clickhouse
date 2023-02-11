from abc import ABC
from typing import List

from validation_service.event import Event
from validation_service.publisher import AbstractMessageProducer


class AbstractEventService(ABC):
    async def publish_event(self, event: Event) -> None:
        raise NotImplementedError


class EventService(AbstractEventService):

    def __init__(self, message_producer: List[AbstractMessageProducer]):
        self._message_producer = message_producer

    async def publish_event(self, event: Event) -> None:
        for producer in self._message_producer:
            await producer.publish(event)

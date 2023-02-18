from abc import ABC

from validation_service.event import Event
from validation_service.publisher import AbstractMessageProducer


class AbstractEventService(ABC):
    async def publish_event(self, event: Event) -> None:
        raise NotImplementedError


class EventService(AbstractEventService):

    def __init__(self, message_producer: AbstractMessageProducer):
        self._message_producer = message_producer

    async def publish_event(self, event: Event) -> None:
        event_utc = event
        event_utc.time = event_utc.time.replace(tzinfo=None)
        await self._message_producer.publish(event_utc)

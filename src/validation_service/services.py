from abc import ABC
from validation_service.event import Event


class AbstractEventService(ABC):
    async def publish_event(self, event: Event) -> None:
        raise NotImplementedError


class EventService(AbstractEventService):
    async def publish_event(self, event: Event) -> None:
        pass


def get_event_service() -> AbstractEventService:
    return EventService()

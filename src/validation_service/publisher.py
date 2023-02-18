import logging
from abc import ABC

from validation_service.event import Event
from validation_service.utils.logconf import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)


class AbstractMessageProducer(ABC):
    async def publish(self, event: Event) -> None:
        raise NotImplementedError

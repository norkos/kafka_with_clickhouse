from validation_service.publisher import RabbitMessageProducer
from validation_service.services import AbstractEventService, EventService


async def get_event_service_with_rabbit() -> AbstractEventService:
    message_publisher = await RabbitMessageProducer.initialize()
    return EventService(message_publisher)

from validation_service.publisher import KafkaMessageProducer
from validation_service.services import AbstractEventService, EventService


async def get_event_service_with_kafka() -> AbstractEventService:
    return EventService(KafkaMessageProducer())

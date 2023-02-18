
from validation_service.services import AbstractEventService, EventService
from validation_service.utils.kafka import KafkaMessageProducer


async def get_event_service_with_kafka() -> AbstractEventService:
    return EventService(KafkaMessageProducer.get_instance())

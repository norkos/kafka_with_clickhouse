from validation_service.publisher import RabbitMessageProducer, KafkaMessageProducer
from validation_service.services import AbstractEventService, EventService


async def get_event_service_with_rabbit() -> AbstractEventService:
    rabbit_message_publisher = await RabbitMessageProducer.initialize()
    kafka_message_publisher = await KafkaMessageProducer.initialize()
    return EventService(
        [rabbit_message_publisher, kafka_message_publisher]
    )

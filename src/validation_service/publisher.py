import asyncio
import logging
from abc import ABC

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, DeliveryMode, ExchangeType

from validation_service.event import Event
from validation_service.utils.logconf import DEFAULT_LOGGER
from validation_service.utils.settings import CLOUDAMQP_URL, ENCODING

logger = logging.getLogger(DEFAULT_LOGGER)


class AbstractMessageProducer(ABC):
    async def publish(self, event: Event):
        raise NotImplementedError


class RabbitMessageProducer(AbstractMessageProducer):
    single_connection = None

    @classmethod
    async def initialize(cls):
        if RabbitMessageProducer.single_connection is None:
            event_loop = asyncio.get_event_loop()
            RabbitMessageProducer.single_connection = await connect_robust(CLOUDAMQP_URL, loop=event_loop)
            logger.info('RabbitMq connection created')
        return cls(RabbitMessageProducer.single_connection)

    def __init__(self, connection: AbstractRobustConnection):
        self._connection = connection

    async def publish(self, event: Event):
        exchange_name = 'topic_events'
        routing_key = 'event'
        channel = await self._connection.channel()
        message_content = event.json()

        exchange = await channel.declare_exchange(name=exchange_name, type=ExchangeType.TOPIC)
        message = Message(message_content.encode(ENCODING), delivery_mode=DeliveryMode.PERSISTENT)
        await exchange.publish(message, routing_key=routing_key)
        logger.debug(f'Sending the event with body={message_content} to routing key={routing_key}')

import asyncio
import json
import logging
from abc import ABC

from aiokafka import AIOKafkaProducer

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, DeliveryMode, ExchangeType
from kafka.errors import KafkaConnectionError

from validation_service.event import Event
from validation_service.utils.logconf import DEFAULT_LOGGER
from validation_service.utils.settings import CLOUDAMQP_URL, ENCODING, KAFKA_URL

logger = logging.getLogger(DEFAULT_LOGGER)


class AbstractMessageProducer(ABC):
    async def publish(self, event: Event) -> None:
        raise NotImplementedError


class KafkaMessageProducer(AbstractMessageProducer):
    producer = None

    @classmethod
    async def initialize(cls):
        if KafkaMessageProducer.producer is None:
            try:
                KafkaMessageProducer.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_URL)
                await KafkaMessageProducer.producer.start()
                logger.info('Kafka connection created')
            except KafkaConnectionError as error:
                logger.error(error)
                raise error
        return cls(KafkaMessageProducer.producer)

    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer
        self._topic = 'topic_events'

    async def publish(self, event: Event) -> None:
        try:
            message_content = json.dumps(event.dict(), default=str).encode(ENCODING)
            await self._producer.send_and_wait(self._topic, message_content)
            logger.debug(f'Sending  the event with body={message_content} to Kafka topic key={self._topic}')
        except Exception as err:
            logger.error(err)
            await self._producer.stop()
            raise err


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
        self._exchange_name = 'topic_events'
        self._routing_key = 'event'

    async def publish(self, event: Event) -> None:
        try:
            channel = await self._connection.channel()
            message_content = event.json()

            exchange = await channel.declare_exchange(name=self._exchange_name, type=ExchangeType.TOPIC)
            message = Message(message_content.encode(ENCODING), delivery_mode=DeliveryMode.PERSISTENT)
            await exchange.publish(message, routing_key=self._routing_key)
            logger.debug(f'Sending the event with body={message_content} to RabbitMQ routing key={self._routing_key}')
        except Exception as err:
            logger.error(err)
            raise err

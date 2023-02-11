from abc import ABC


class MessageProducer(ABC):
    async def publish(self):
        raise NotImplementedError

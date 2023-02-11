import logging
from logging.config import dictConfig

from fastapi import FastAPI
import uvicorn

from validation_service.api import router
from validation_service.utils.kafka import Kafka
from validation_service.utils.settings import PORT, DEBUG_LOGGER_LEVEL, KAFKA_TOPIC, KAFKA_URL
from validation_service.utils.logconf import log_config, DEFAULT_LOGGER

dictConfig(log_config)

logger = logging.getLogger(DEFAULT_LOGGER)

kafka_server = Kafka(
    topic=KAFKA_TOPIC,
    connection=KAFKA_URL
)

app = FastAPI(
    debug=DEBUG_LOGGER_LEVEL,
    title='blockchain-service',
    docs_url='/_swagger'
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    logger.info(f'Application started with debugging: {DEBUG_LOGGER_LEVEL}')
    await kafka_server.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_server.stop()


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=PORT,
        workers=1
    )

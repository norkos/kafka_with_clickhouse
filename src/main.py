import logging
from logging.config import dictConfig

from fastapi import FastAPI
import uvicorn

from validation_service.api import router
from validation_service.utils.kafka import KafkaMessageProducer
from validation_service.utils.settings import PORT, DEBUG_LOGGER_LEVEL
from validation_service.utils.logconf import log_config, DEFAULT_LOGGER
from validation_service.clickhouse import create_table

dictConfig(log_config)

logger = logging.getLogger(DEFAULT_LOGGER)

app = FastAPI(
    debug=DEBUG_LOGGER_LEVEL,
    title='blockchain-service',
    docs_url='/_swagger'
)

app.include_router(router)


kafka = KafkaMessageProducer.get_instance()


@app.on_event("startup")
async def startup():
    logger.info(f'Application started with debugging: {DEBUG_LOGGER_LEVEL}')
    await kafka.start()
    create_table()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.stop()


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=PORT,
        workers=1
    )

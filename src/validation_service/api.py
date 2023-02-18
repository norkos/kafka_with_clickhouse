import logging
from fastapi import APIRouter, Depends

from validation_service.dependecies import get_event_service_with_kafka
from validation_service.services import AbstractEventService
from validation_service.event import Event
from validation_service.utils.logconf import DEFAULT_LOGGER
from validation_service.clickhouse import get_data

logger = logging.getLogger(DEFAULT_LOGGER)

router = APIRouter(
    prefix='/api'
)


@router.post("/event", response_model=Event)
async def create_event(event: Event, event_service: AbstractEventService = Depends(get_event_service_with_kafka)):
    logger.debug(f'Received request: {event}')
    await event_service.publish_event(event)
    return event


@router.get("/report")
async def report():
    get_data()
    return {"message": 'todo'}

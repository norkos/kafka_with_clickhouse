import logging
from fastapi import APIRouter, Depends

from validation_service.services import AbstractEventService, get_event_service
from validation_service.event import Event
from validation_service.utils.logconf import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)

router = APIRouter(
    prefix='/api'
)


@router.post("/event", response_model=Event)
async def create_event(event: Event, event_service: AbstractEventService = Depends(get_event_service)):
    logger.debug(f'Received event: {event}')
    await event_service.publish_event(event)
    return event


@router.get("/report")
async def report():
    return {"message": "Hello World"}
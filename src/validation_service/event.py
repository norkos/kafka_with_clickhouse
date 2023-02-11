from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import uuid


class Type(str, Enum):
    validate = 'validate'
    accept = 'accept'


class Event(BaseModel):
    time: datetime
    correlation_id: uuid.UUID
    check_id: uuid.UUID
    type: Type

<<<<<<< HEAD
from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional

class ScheduleCreateSchema(BaseModel):
    bus_id: int
    route_id: int
    departure_time: datetime
    arrival_time: datetime
    status: Optional[str] = 'active'

class ScheduleUpdateSchema(BaseModel):
    bus_id: Optional[int]
    route_id: Optional[int]
    departure_time: Optional[datetime]
    arrival_time: Optional[datetime]
    status: Optional[str]
=======
from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional

class ScheduleCreateSchema(BaseModel):
    bus_id: int
    route_id: int
    departure_time: datetime
    arrival_time: datetime
    status: Optional[str] = 'active'

class ScheduleUpdateSchema(BaseModel):
    bus_id: Optional[int]
    route_id: Optional[int]
    departure_time: Optional[datetime]
    arrival_time: Optional[datetime]
    status: Optional[str]
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0

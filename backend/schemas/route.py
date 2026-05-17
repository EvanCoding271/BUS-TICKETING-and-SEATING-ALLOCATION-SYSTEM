<<<<<<< HEAD
from pydantic import BaseModel, constr
from typing import Optional

class RouteCreateSchema(BaseModel):
    name: constr(min_length=3)
    origin: constr(min_length=2)
    destination: constr(min_length=2)
    base_fare: float
    status: Optional[str] = 'active'

class RouteUpdateSchema(BaseModel):
    name: Optional[constr(min_length=3)]
    origin: Optional[constr(min_length=2)]
    destination: Optional[constr(min_length=2)]
    base_fare: Optional[float]
    status: Optional[str]
=======
from pydantic import BaseModel, constr
from typing import Optional

class RouteCreateSchema(BaseModel):
    name: constr(min_length=3)
    origin: constr(min_length=2)
    destination: constr(min_length=2)
    base_fare: float
    status: Optional[str] = 'active'

class RouteUpdateSchema(BaseModel):
    name: Optional[constr(min_length=3)]
    origin: Optional[constr(min_length=2)]
    destination: Optional[constr(min_length=2)]
    base_fare: Optional[float]
    status: Optional[str]
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0

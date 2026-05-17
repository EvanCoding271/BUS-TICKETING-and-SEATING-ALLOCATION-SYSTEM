<<<<<<< HEAD
from pydantic import BaseModel, constr
from typing import List

class BookingReserveSchema(BaseModel):
    user_id: int
    schedule_id: int
    seat_labels: List[constr(min_length=2)]
    payment_method: constr(min_length=3)

class BookingConfirmSchema(BaseModel):
    booking_id: int
    payment_method: constr(min_length=3)
=======
from pydantic import BaseModel, constr
from typing import List

class BookingReserveSchema(BaseModel):
    user_id: int
    schedule_id: int
    seat_labels: List[constr(min_length=2)]
    payment_method: constr(min_length=3)

class BookingConfirmSchema(BaseModel):
    booking_id: int
    payment_method: constr(min_length=3)
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0

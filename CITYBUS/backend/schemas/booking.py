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

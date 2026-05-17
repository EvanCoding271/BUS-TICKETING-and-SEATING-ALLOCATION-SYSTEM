<<<<<<< HEAD
from pydantic import BaseModel, constr

class PaymentProcessSchema(BaseModel):
    booking_id: int
    amount: float
    method: constr(min_length=3)

class RefundSchema(BaseModel):
    booking_id: int
    amount: float
    reason: constr(min_length=5)
=======
from pydantic import BaseModel, constr

class PaymentProcessSchema(BaseModel):
    booking_id: int
    amount: float
    method: constr(min_length=3)

class RefundSchema(BaseModel):
    booking_id: int
    amount: float
    reason: constr(min_length=5)
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0

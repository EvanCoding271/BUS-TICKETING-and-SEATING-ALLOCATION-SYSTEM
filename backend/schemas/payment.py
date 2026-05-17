from pydantic import BaseModel, constr

class PaymentProcessSchema(BaseModel):
    booking_id: int
    amount: float
    method: constr(min_length=3)

class RefundSchema(BaseModel):
    booking_id: int
    amount: float
    reason: constr(min_length=5)

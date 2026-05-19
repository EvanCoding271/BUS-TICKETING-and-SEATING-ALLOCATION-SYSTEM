from fastapi import APIRouter, HTTPException, Depends
from ..schemas.payment import PaymentProcessSchema, RefundSchema
from ..auth.role_guard import require_role, require_any_role
from ..database.connection import database

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/process", dependencies=[Depends(require_role("passenger"))])
async def process_payment(payload: PaymentProcessSchema):
    booking = await database.fetch_one("SELECT id, payment_status FROM bookings WHERE id = :id", values={"id": payload.booking_id})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking["payment_status"] == "paid":
        raise HTTPException(status_code=409, detail="Payment already processed")
    await database.execute(
        "INSERT INTO payments (booking_id, amount, method, status, paid_at, created_at) VALUES (:booking_id, :amount, :method, 'completed', now(), now())",
        values={"booking_id": payload.booking_id, "amount": payload.amount, "method": payload.method}
    )
    await database.execute("UPDATE bookings SET payment_status = 'paid', booking_status = 'confirmed', updated_at = now() WHERE id = :id", values={"id": payload.booking_id})
    return {"status": "paid"}

@router.post("/refund", dependencies=[Depends(require_any_role(["finance", "admin"]))])
async def process_refund(payload: RefundSchema):
    booking = await database.fetch_one("SELECT id FROM bookings WHERE id = :id", values={"id": payload.booking_id})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await database.execute(
        "INSERT INTO refund_logs (booking_id, amount, reason, status, created_at) VALUES (:booking_id, :amount, :reason, 'processed', now())",
        values={"booking_id": payload.booking_id, "amount": payload.amount, "reason": payload.reason}
    )
    await database.execute("UPDATE bookings SET booking_status = 'refunded', updated_at = now() WHERE id = :id", values={"id": payload.booking_id})
    return {"status": "refunded"}

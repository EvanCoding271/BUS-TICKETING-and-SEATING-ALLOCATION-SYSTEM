from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..utils.qr_generator import generate_qr_base64
from ..database.connection import database

router = APIRouter(prefix="/qr", tags=["qr"])

class QRRequest(BaseModel):
    qr_payload: str

@router.post("/generate/{booking_id}")
async def generate_ticket(booking_id: int):
    booking = await database.fetch_one("SELECT id FROM bookings WHERE id = :id", values={"id": booking_id})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    qr_code = f"ticket:{booking_id}:{int(booking_id * 7919)}"
    qr_image = generate_qr_base64(qr_code)
    await database.execute(
        "INSERT INTO tickets (booking_id, qr_code, ticket_status, issued_at, created_at) VALUES (:booking_id, :qr_code, 'issued', now(), now())",
        values={"booking_id": booking_id, "qr_code": qr_code}
    )
    return {"booking_id": booking_id, "qr_image": qr_image}

@router.post("/validate")
async def validate_qr(payload: QRRequest):
    ticket = await database.fetch_one("SELECT id, ticket_status FROM tickets WHERE qr_code = :qr_code", values={"qr_code": payload.qr_payload})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket["ticket_status"] != 'issued':
        raise HTTPException(status_code=409, detail="Ticket already used or invalid")
    await database.execute("UPDATE tickets SET ticket_status = 'used', used_at = now(), updated_at = now() WHERE id = :id", values={"id": ticket["id"]})
    return {"status": "validated"}


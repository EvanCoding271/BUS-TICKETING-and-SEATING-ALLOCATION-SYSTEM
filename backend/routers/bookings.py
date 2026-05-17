from fastapi import APIRouter, HTTPException, Depends
from ..database.connection import database
from ..auth.role_guard import require_role, require_any_role
from ..schemas.booking import BookingReserveSchema, BookingConfirmSchema

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/reserve", dependencies=[Depends(require_role("passenger"))])
async def reserve(payload: BookingReserveSchema, current_user: dict = Depends(require_role("passenger"))):
    async with database.transaction():
        seat_query = "SELECT id, seat_label, status FROM seats WHERE schedule_id = :schedule_id AND seat_label = ANY(:seat_labels) FOR UPDATE"
        seats = await database.fetch_all(seat_query, values={"schedule_id": payload.schedule_id, "seat_labels": payload.seat_labels})
        if len(seats) != len(payload.seat_labels) or any(seat["status"] != 'available' for seat in seats):
            raise HTTPException(status_code=409, detail="One or more seats are not available")

        fare_data = await database.fetch_one(
            "SELECT base_fare FROM routes WHERE id = (SELECT route_id FROM schedules WHERE id = :schedule_id)",
            values={"schedule_id": payload.schedule_id}
        )
        if not fare_data:
            raise HTTPException(status_code=404, detail="Route fare not found")

        fare_amount = float(fare_data["base_fare"] or 0) * len(payload.seat_labels)
        booking_q = "INSERT INTO bookings (user_id, schedule_id, booking_date, booking_status, payment_status, total_amount) VALUES (:user_id, :schedule_id, now(), 'pending', 'pending', :total_amount) RETURNING id"
        booking_id = await database.execute(booking_q, values={
            "user_id": current_user["sub"],
            "schedule_id": payload.schedule_id,
            "total_amount": fare_amount
        })
        for seat_label in payload.seat_labels:
            matching = next((seat for seat in seats if seat["seat_label"] == seat_label), None)
            if not matching:
                raise HTTPException(status_code=404, detail=f"Seat {seat_label} not found")
            await database.execute(
                "INSERT INTO booking_seats (booking_id, seat_id, seat_label) VALUES (:booking_id, :seat_id, :seat_label)",
                values={"booking_id": booking_id, "seat_id": matching["id"], "seat_label": seat_label}
            )
            await database.execute("UPDATE seats SET status = 'reserved', updated_at = now() WHERE id = :id", values={"id": matching["id"]})
        return {"booking_id": booking_id, "total_amount": fare_amount}

@router.post("/confirm", dependencies=[Depends(require_role("passenger"))])
async def confirm_booking(payload: BookingConfirmSchema, current_user: dict = Depends(require_role("passenger"))):
    booking = await database.fetch_one("SELECT id, payment_status, user_id FROM bookings WHERE id = :id", values={"id": payload.booking_id})
    if not booking or booking["user_id"] != current_user["sub"]:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking["payment_status"] == 'paid':
        raise HTTPException(status_code=409, detail="Booking already paid")
    await database.execute(
        "INSERT INTO payments (booking_id, amount, method, status, paid_at, created_at) VALUES (:booking_id, (SELECT total_amount FROM bookings WHERE id = :booking_id), :method, 'completed', now(), now())",
        values={"booking_id": payload.booking_id, "method": payload.payment_method}
    )
    await database.execute(
        "UPDATE bookings SET payment_status = 'paid', booking_status = 'confirmed', updated_at = now() WHERE id = :id",
        values={"id": payload.booking_id}
    )
    return {"booking_id": payload.booking_id, "status": "confirmed"}

@router.get("/history", dependencies=[Depends(require_role("passenger"))])
async def booking_history(current_user: dict = Depends(require_role("passenger"))):
    query = """
      SELECT b.id, b.schedule_id, b.booking_status, b.payment_status, b.total_amount, b.booking_date,
             r.origin, r.destination
      FROM bookings b
      JOIN schedules s ON s.id = b.schedule_id
      JOIN routes r ON r.id = s.route_id
      WHERE b.user_id = :user_id
      ORDER BY b.booking_date DESC
    """
    return await database.fetch_all(query, values={"user_id": current_user["sub"]})

@router.get("/assigned", dependencies=[Depends(require_any_role(["operator", "admin"]))])
async def assigned_trips():
    query = "SELECT id, bus_id, route_id, departure_time, arrival_time, status FROM schedules WHERE status = 'active' ORDER BY departure_time"
    return await database.fetch_all(query)

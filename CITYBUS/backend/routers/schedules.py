from fastapi import APIRouter, HTTPException, Depends
from ..schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema
from ..auth.role_guard import require_role
from ..database.connection import database

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.get("/list")
async def list_schedules():
    return await database.fetch_all("SELECT id, bus_id, route_id, departure_time, arrival_time, status FROM schedules ORDER BY departure_time")

@router.post("/create", dependencies=[Depends(require_role("admin"))])
async def create_schedule(payload: ScheduleCreateSchema):
    query = "INSERT INTO schedules (bus_id, route_id, departure_time, arrival_time, status, created_at) VALUES (:bus_id, :route_id, :departure_time, :arrival_time, :status, now()) RETURNING id"
    schedule_id = await database.execute(query, values=payload.dict())
    return {"id": schedule_id}

@router.patch("/{schedule_id}", dependencies=[Depends(require_role("admin"))])
async def update_schedule(schedule_id: int, payload: ScheduleUpdateSchema):
    existing = await database.fetch_one("SELECT id FROM schedules WHERE id = :id", values={"id": schedule_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")
    values = {**payload.dict(exclude_unset=True), "id": schedule_id}
    set_sql = ", ".join([f"{k} = :{k}" for k in payload.dict(exclude_unset=True).keys()])
    if set_sql:
        await database.execute(f"UPDATE schedules SET {set_sql}, updated_at = now() WHERE id = :id", values=values)
    return {"status": "updated"}

@router.delete("/{schedule_id}", dependencies=[Depends(require_role("admin"))])
async def delete_schedule(schedule_id: int):
    await database.execute("DELETE FROM schedules WHERE id = :id", values={"id": schedule_id})
    return {"status": "deleted"}

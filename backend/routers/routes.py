from fastapi import APIRouter, HTTPException, Depends
from schemas.route import RouteCreateSchema, RouteUpdateSchema
from auth.role_guard import require_role
from database.connection import database

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/list")
async def list_routes():
    query = "SELECT id, name, origin, destination, base_fare, status FROM routes ORDER BY id"
    return await database.fetch_all(query)

@router.get("/{route_id}")
async def get_route(route_id: int):
    query = "SELECT id, name, origin, destination, base_fare, status FROM routes WHERE id = :id"
    route = await database.fetch_one(query, values={"id": route_id})
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.post("/create", dependencies=[Depends(require_role("admin"))])
async def create_route(payload: RouteCreateSchema):
    query = "INSERT INTO routes (name, origin, destination, base_fare, status, created_at) VALUES (:name, :origin, :destination, :base_fare, :status, now()) RETURNING id"
    route_id = await database.execute(query, values=payload.dict())
    return {"id": route_id}

@router.patch("/{route_id}", dependencies=[Depends(require_role("admin"))])
async def update_route(route_id: int, payload: RouteUpdateSchema):
    existing = await database.fetch_one("SELECT id FROM routes WHERE id = :id", values={"id": route_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Route not found")
    values = {**payload.dict(exclude_unset=True), "id": route_id}
    set_sql = ", ".join([f"{k} = :{k}" for k in payload.dict(exclude_unset=True).keys()])
    if set_sql:
        await database.execute(f"UPDATE routes SET {set_sql}, updated_at = now() WHERE id = :id", values=values)
    return {"status": "updated"}

@router.delete("/{route_id}", dependencies=[Depends(require_role("admin"))])
async def delete_route(route_id: int):
    await database.execute("DELETE FROM routes WHERE id = :id", values={"id": route_id})
    return {"status": "deleted"}

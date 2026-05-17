from fastapi import APIRouter, Depends
from ..schemas.finance import FinanceReportRequest
from ..auth.role_guard import require_any_role
from ..database.connection import database

router = APIRouter(prefix="/finance", tags=["finance"])

@router.get("/summary", dependencies=[Depends(require_any_role(["finance", "admin"]))])
async def finance_summary():
    revenue = await database.fetch_one("SELECT COALESCE(SUM(amount),0)::numeric AS total FROM payments")
    refunds = await database.fetch_one("SELECT COALESCE(SUM(amount),0)::numeric AS total FROM refund_logs")
    return {
        "total_revenue": float(revenue["total"] or 0),
        "total_refunds": float(refunds["total"] or 0),
        "net_revenue": float((revenue["total"] or 0) - (refunds["total"] or 0))
    }

@router.post("/reports", dependencies=[Depends(require_any_role(["finance", "admin"]))])
async def export_reports(payload: FinanceReportRequest):
    return {"status": "generated", "from": payload.from_date, "to": payload.to_date, "type": payload.report_type}

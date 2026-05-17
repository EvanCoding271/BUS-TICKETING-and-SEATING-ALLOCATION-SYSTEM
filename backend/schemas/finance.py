from pydantic import BaseModel
from typing import Optional

class FinanceReportRequest(BaseModel):
    from_date: Optional[str]
    to_date: Optional[str]
    report_type: Optional[str] = 'summary'

<<<<<<< HEAD
from pydantic import BaseModel
from typing import Optional

class FinanceReportRequest(BaseModel):
    from_date: Optional[str]
    to_date: Optional[str]
    report_type: Optional[str] = 'summary'
=======
from pydantic import BaseModel
from typing import Optional

class FinanceReportRequest(BaseModel):
    from_date: Optional[str]
    to_date: Optional[str]
    report_type: Optional[str] = 'summary'
>>>>>>> a96f8434797859db5b8f2889941570f4dc9b35d0

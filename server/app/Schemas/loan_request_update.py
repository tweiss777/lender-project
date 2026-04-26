from pydantic import BaseModel
from typing import Optional

from app.models.LoanRequest import LoanRequestStatus
class LoanRequestUpdate(BaseModel):
    borrower_id: Optional[int] = None
    amount: Optional[float] = None
    term_months: Optional[int] = None
    equipment_type: Optional[str] = None
    equipment_year: Optional[int] = None
    equipment_cost: Optional[float] = None
    equipment_description: Optional[str] = None
    status: Optional[LoanRequestStatus] = None
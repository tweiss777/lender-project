from pydantic import BaseModel

from app.models.LoanRequest import LoanRequestStatus


class LoanRequestCreate(BaseModel):
    borrower_id: int
    amount: float
    term_months: int
    equipment_type: str
    equipment_year: int
    equipment_cost: float
    equipment_description: str
    status: LoanRequestStatus

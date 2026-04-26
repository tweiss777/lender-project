from pydantic import BaseModel

class BorrowCreate(BaseModel):
    company_name: str
    industry: str
    state: str
    years_in_business: int
    revenue: float

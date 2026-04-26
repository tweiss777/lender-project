from typing import Optional
from pydantic import BaseModel

class BorrowUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    state: Optional[str] = None
    years_in_business: Optional[int] = None
    revenue: Optional[float] = None

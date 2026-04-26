from typing import Optional
from pydantic import BaseModel


class LenderPolicyPreview(BaseModel):
    """
    Represents one parsed program from a lender PDF.
    Returned to the user for review before being committed to the database.
    """
    program_name: str

    # Loan constraints
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None
    min_term_months: Optional[int] = None
    max_term_months: Optional[int] = None

    # Credit scores
    min_fico: Optional[int] = None
    min_paynet_score: Optional[float] = None

    # Business requirements
    min_years_in_business: Optional[int] = None
    min_revenue: Optional[float] = None

    # Equipment
    max_equipment_age_years: Optional[int] = None
    equipment_restrictions: list[str] = []

    # Geography
    allowed_states: list[str] = []
    excluded_states: list[str] = []

    # Industry
    allowed_industries: list[str] = []
    excluded_industries: list[str] = []

    # Credit history
    no_bankruptcy: Optional[bool] = None
    min_years_since_bankruptcy: Optional[int] = None
    allows_judgments: Optional[bool] = None
    allows_liens: Optional[bool] = None
    requires_us_citizen: Optional[bool] = None


class LenderPreview(BaseModel):
    """
    Full preview returned after parsing a PDF.
    Contains the lender name and all parsed programs.
    """
    lender_name: str
    programs: list[LenderPolicyPreview]

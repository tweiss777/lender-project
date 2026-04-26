from app.Schemas.loan_request_create import LoanRequestCreate


class LoanRequestResponse(LoanRequestCreate):
    loan_request_id: int

    class Config:
        from_attributes = True
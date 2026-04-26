from app.Schemas.borrow_create import BorrowCreate


class BorrowerResponse(BorrowCreate):
    borrower_id: int

    class Config:
        from_attributes = True
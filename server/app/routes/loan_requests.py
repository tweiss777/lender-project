from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException
from app.Schemas.loan_request_response import LoanRequestResponse
from app.Schemas.loan_request_update import LoanRequestUpdate
from app.database import get_db 

from app.Schemas.loan_request_create import LoanRequestCreate
from app.models.LoanRequest import LoanRequest

loan_requests_routes = APIRouter()


@loan_requests_routes.post('/', response_model=LoanRequestResponse, status_code=201)
def create_loan_request(loan_request: LoanRequestCreate, db: Session = Depends(get_db)):
    new_db_loan_request = LoanRequest(**loan_request.model_dump()) 
    db.add(new_db_loan_request)
    db.commit()
    db.refresh(new_db_loan_request)
    return new_db_loan_request


@loan_requests_routes.get('/{loan_request_id}', response_model=LoanRequestResponse)
def get_loan_request(loan_request_id: int, db: Session = Depends(get_db)):
    existing_loan_request = db.query(LoanRequest).filter(LoanRequest.loan_request_id == loan_request_id).first()
    if not existing_loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    return existing_loan_request


@loan_requests_routes.patch('/{loan_request_id}', status_code=204)
def patch_loan_request(loan_request_id: int, loan_requests_update: LoanRequestUpdate, db: Session = Depends(get_db)):
    existing_loan_request = db.query(LoanRequest).filter(LoanRequest.loan_request_id == loan_request_id).first()
    if not existing_loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found.")
    for field, value in loan_requests_update.model_dump(exclude_none=True).items():
        setattr(existing_loan_request, field, value)
    db.commit()
    db.refresh(existing_loan_request) 


@loan_requests_routes.delete('/{loan_request_id}', status_code=204)
def delete_loan_request(loan_request_id: int, db: Session = Depends(get_db)):
    existing_loan_request = db.query(LoanRequest).filter(LoanRequest.loan_request_id == loan_request_id).first()
    if not existing_loan_request:
        raise HTTPException(status_code=404, detail='Loan request not found')
    db.delete(existing_loan_request)
    db.commit()
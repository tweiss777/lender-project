from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.Schemas.underwriter_request import UnderWriterRequest
from app.database import get_db 
from app.models.Borrower import Borrower
from app.models.Lender import Lender
from app.models.LenderPolicy import LenderPolicy
from app.models.LoanRequest import LoanRequest
from app.models.MatchResult import MatchResult
from app.Schemas.borrow_create import BorrowCreate
from app.Schemas.borrow_update import BorrowUpdate
from app.Schemas.borrower_response import BorrowerResponse
from app.Schemas.underwriter_response import UnderwriterResponse
from app.services.matching_engine import MatchingEngine

borrower_routes = APIRouter()


@borrower_routes.post('/', response_model=BorrowerResponse, status_code=201)
def create_borrower(borrower: BorrowCreate, db: Session = Depends(get_db)):
    new_db_borrower = Borrower(**borrower.model_dump())
    db.add(new_db_borrower)
    db.commit()
    db.refresh(new_db_borrower)
    return new_db_borrower


@borrower_routes.get('/{borrower_id}', response_model=BorrowerResponse)
def get_borrower(borrower_id: int, db: Session = Depends(get_db)):
    borrower = db.query(Borrower).filter(Borrower.borrower_id == borrower_id).first()
    if not borrower:
        raise HTTPException(status_code=404, detail='Borrower not found')
    return borrower


@borrower_routes.patch('/{borrower_id}', response_model=BorrowerResponse)
def patch_borrower(borrower_id: int, updates: BorrowUpdate, db: Session = Depends(get_db)):
    existing_borrower = db.query(Borrower).filter(Borrower.borrower_id == borrower_id).first()
    if not existing_borrower:
        raise HTTPException(status_code=404, detail='Borrower not found')
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(existing_borrower, field, value)
    db.commit()
    db.refresh(existing_borrower)
    return existing_borrower


@borrower_routes.delete('/{borrower_id}', status_code=204)
def delete_borrower(borrower_id: int, db: Session = Depends(get_db)):
    existing_borrower = db.query(Borrower).filter(Borrower.borrower_id == borrower_id).first()
    if not existing_borrower:
        raise HTTPException(status_code=404, detail='Borrower not found')
    db.delete(existing_borrower)
    db.commit()



@borrower_routes.post('/{borrower_id}/underwrite', response_model=list[UnderwriterResponse], status_code=201)
def create_underwrite_result(borrower_id: int, request: UnderWriterRequest, db: Session = Depends(get_db)):
    if not db.query(Borrower).filter(Borrower.borrower_id == borrower_id).first():
        raise HTTPException(status_code=404, detail='Borrower not found')

    loan_request = db.query(LoanRequest).filter(
        LoanRequest.loan_request_id == request.loan_request_id,
        LoanRequest.borrower_id == borrower_id,
    ).first()
    if not loan_request:
        raise HTTPException(status_code=404, detail='Loan request not found or does not belong to this borrower')

    MatchingEngine().run(loan_request_id=request.loan_request_id, db=db)

    rows = (
        db.query(MatchResult, LenderPolicy, Lender)
        .join(LenderPolicy, MatchResult.policy_id == LenderPolicy.policy_id)
        .join(Lender, LenderPolicy.lender_id == Lender.lender_id)
        .filter(MatchResult.loan_request_id == request.loan_request_id)
        .all()
    )

    return [
        UnderwriterResponse(
            match_id=match.match_id,
            loan_request_id=match.loan_request_id,
            lender_name=lender.lender_name,
            program_name=policy.program_name,
            is_eligible=match.is_eligible,
            match_score=match.match_score,
            status=match.status,
            criteria_results=match.criteria_results,
        )
        for match, policy, lender in rows
    ]


@borrower_routes.get('/{borrower_id}/underwrite', response_model=list[UnderwriterResponse])
def get_underwrite_results(borrower_id: int, db: Session = Depends(get_db)):
    existing_borrower = db.query(Borrower).filter(Borrower.borrower_id == borrower_id).first()
    if not existing_borrower:
        raise HTTPException(status_code=404, detail='Borrower not found')

    rows = (
        db.query(MatchResult, LenderPolicy, Lender)
        .join(LenderPolicy, MatchResult.policy_id == LenderPolicy.policy_id)
        .join(Lender, LenderPolicy.lender_id == Lender.lender_id)
        .join(LoanRequest, MatchResult.loan_request_id == LoanRequest.loan_request_id)
        .filter(LoanRequest.borrower_id == borrower_id)
        .all()
    )

    return [
        UnderwriterResponse(
            match_id=match.match_id,
            loan_request_id=match.loan_request_id,
            lender_name=lender.lender_name,
            program_name=policy.program_name,
            is_eligible=match.is_eligible,
            match_score=match.match_score,
            status=match.status,
            criteria_results=match.criteria_results,
        )
        for match, policy, lender in rows
    ]

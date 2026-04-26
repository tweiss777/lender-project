import enum
from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base


class LoanRequestStatus(enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'
    funded = 'funded'


class LoanRequest(Base):
    __tablename__ = 'loan_requests'

    loan_request_id = Column('loan_request_id', Integer, primary_key=True)
    borrower_id = Column('borrower_id', Integer, ForeignKey('borrowers.borrower_id'))
    amount = Column('amount', Float)
    term_months = Column('term_months', Integer)
    equipment_type = Column('equipment_type', VARCHAR)
    # Model year of the equipment — required for age-based checks (e.g. Apex max 15yr)
    equipment_year = Column('equipment_year', Integer)
    equipment_cost = Column('equipment_cost', Float)
    equipment_description = Column('equipment_description', VARCHAR)
    status = Column('status', Enum(LoanRequestStatus), nullable=False)

    borrower = relationship('Borrower', back_populates='loan_requests')
    match_results = relationship('MatchResult', back_populates='loan_request', cascade='all, delete-orphan')

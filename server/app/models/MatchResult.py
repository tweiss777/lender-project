import enum
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base


class MatchStatus(enum.Enum):
    eligible = 'eligible'
    ineligible = 'ineligible'


class MatchResult(Base):
    __tablename__ = 'match_results'

    match_id = Column('match_id', Integer, primary_key=True, autoincrement=True)
    loan_request_id = Column('loan_request_id', Integer, ForeignKey('loan_requests.loan_request_id'), nullable=False)
    policy_id = Column('policy_id', Integer, ForeignKey('lender_policies.policy_id'), nullable=False)

    # True if every applicable criterion passed
    is_eligible = Column('is_eligible', Boolean, nullable=False)

    # 0–100: percentage of applicable criteria that passed
    match_score = Column('match_score', Float, nullable=False)

    status = Column('status', Enum(MatchStatus), nullable=False)

    # Per-criterion detail for the UI:
    # [{"name": "FICO Score", "passed": true, "reason": "FICO 740 meets minimum of 700"}, ...]
    criteria_results = Column('criteria_results', JSON, nullable=False)

    loan_request = relationship('LoanRequest', back_populates='match_results')
    policy = relationship('LenderPolicy', back_populates='match_results')

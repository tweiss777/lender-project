from sqlalchemy import Column, Integer, VARCHAR, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class LenderPolicy(Base):
    __tablename__ = 'lender_policies'

    policy_id = Column('policy_id', Integer, primary_key=True)
    lender_id = Column('lender_id', Integer, ForeignKey('lenders.lender_id'), nullable=False)
    program_name = Column('program_name', VARCHAR)

    # Loan constraints
    min_loan_amount = Column('min_loan_amount', Float)
    max_loan_amount = Column('max_loan_amount', Float)
    min_term_months = Column('min_term_months', Integer)
    max_term_months = Column('max_term_months', Integer)

    # Credit scores
    min_fico = Column('min_fico', Integer)
    min_paynet_score = Column('min_paynet_score', Float)

    # Business requirements
    min_years_in_business = Column('min_years_in_business', Integer)
    min_revenue = Column('min_revenue', Float)

    # Equipment
    # Maximum age of equipment in years (e.g. Apex: 15, Falcon trucking: 10)
    max_equipment_age_years = Column('max_equipment_age_years', Integer)

    # Credit history
    # True  → lender accepts NO prior bankruptcies (e.g. Advantage+)
    no_bankruptcy = Column('no_bankruptcy', Boolean)
    # Minimum years since discharge required (e.g. Falcon: 15, Stearns: 7, Citizens: 5)
    min_years_since_bankruptcy = Column('min_years_since_bankruptcy', Integer)
    # False → lender explicitly rejects applicants with judgments (e.g. Advantage+)
    allows_judgments = Column('allows_judgments', Boolean)
    # False → lender explicitly rejects applicants with tax liens (e.g. Advantage+)
    allows_liens = Column('allows_liens', Boolean)

    # Misc
    requires_us_citizen = Column('requires_us_citizen', Boolean)

    lender = relationship('Lender', back_populates='policies')
    allowed_industries = relationship('LenderAllowedIndustry', cascade='all, delete-orphan')
    allowed_states = relationship('LenderAllowedState', cascade='all, delete-orphan')
    excluded_industries = relationship('LenderExcludedIndustry', cascade='all, delete-orphan')
    excluded_states = relationship('LenderExcludedState', cascade='all, delete-orphan')
    equipment_restrictions = relationship('LenderEquipmentRestriction', cascade='all, delete-orphan')
    match_results = relationship('MatchResult', back_populates='policy')

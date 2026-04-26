from typing import Optional
from sqlalchemy import Integer, VARCHAR, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base


class LenderPolicy(Base):
    __tablename__ = 'lender_policies'

    policy_id: Mapped[int] = mapped_column('policy_id', Integer, primary_key=True)
    lender_id: Mapped[int] = mapped_column('lender_id', Integer, ForeignKey('lenders.lender_id'), nullable=False)
    program_name: Mapped[Optional[str]] = mapped_column('program_name', VARCHAR)

    # Loan constraints
    min_loan_amount: Mapped[Optional[float]] = mapped_column('min_loan_amount', Float)
    max_loan_amount: Mapped[Optional[float]] = mapped_column('max_loan_amount', Float)
    min_term_months: Mapped[Optional[int]] = mapped_column('min_term_months', Integer)
    max_term_months: Mapped[Optional[int]] = mapped_column('max_term_months', Integer)

    # Credit scores
    min_fico: Mapped[Optional[int]] = mapped_column('min_fico', Integer)
    min_paynet_score: Mapped[Optional[float]] = mapped_column('min_paynet_score', Float)

    # Business requirements
    min_years_in_business: Mapped[Optional[int]] = mapped_column('min_years_in_business', Integer)
    min_revenue: Mapped[Optional[float]] = mapped_column('min_revenue', Float)

    # Equipment
    max_equipment_age_years: Mapped[Optional[int]] = mapped_column('max_equipment_age_years', Integer)

    # Credit history
    no_bankruptcy: Mapped[Optional[bool]] = mapped_column('no_bankruptcy', Boolean)
    min_years_since_bankruptcy: Mapped[Optional[int]] = mapped_column('min_years_since_bankruptcy', Integer)
    allows_judgments: Mapped[Optional[bool]] = mapped_column('allows_judgments', Boolean)
    allows_liens: Mapped[Optional[bool]] = mapped_column('allows_liens', Boolean)

    # Misc
    requires_us_citizen: Mapped[Optional[bool]] = mapped_column('requires_us_citizen', Boolean)

    lender = relationship('Lender', back_populates='policies')
    allowed_industries = relationship('LenderAllowedIndustry', cascade='all, delete-orphan')
    allowed_states = relationship('LenderAllowedState', cascade='all, delete-orphan')
    excluded_industries = relationship('LenderExcludedIndustry', cascade='all, delete-orphan')
    excluded_states = relationship('LenderExcludedState', cascade='all, delete-orphan')
    equipment_restrictions = relationship('LenderEquipmentRestriction', cascade='all, delete-orphan')
    match_results = relationship('MatchResult', back_populates='policy')

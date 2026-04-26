# Borrower/Business (industry, state, years in business, revenue)
from sqlalchemy import Column, Integer, VARCHAR, CHAR, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class Borrower(Base):
    __tablename__ = 'borrowers'
    borrower_id = Column('borrower_id', Integer, primary_key=True)
    company_name = Column('company_name', VARCHAR)
    industry = Column('industry', VARCHAR)
    state = Column('state', CHAR(2))
    years_in_business = Column('years_in_business', Integer)
    revenue = Column('revenue', Float)

    loan_requests = relationship('LoanRequest', back_populates='borrower', cascade='all, delete-orphan')
    business_credit = relationship('BusinessCredit', back_populates='borrower', cascade='all, delete-orphan', uselist=False)
    guarantors = relationship('PersonalGuarantor', back_populates='borrower', cascade='all, delete-orphan')

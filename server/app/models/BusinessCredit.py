# BusinessCredit (PayNet score, trade lines)
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class BusinessCredit(Base):
    __tablename__ = 'business_credits'
    bc_id = Column('bc_id', Integer, primary_key=True)
    borrower_id = Column('borrower_id', Integer, ForeignKey('borrowers.borrower_id'))
    paynet_score = Column('paynet_score', Float)
    trade_lines = Column('trade_lines', Integer)
    days_beyond_terms = Column('days_beyond_terms', Float)
    high_credit = Column('high_credit', Float)
    derogatory_marks = Column('derogatory_marks', Integer)

    borrower = relationship('Borrower', back_populates='business_credit')

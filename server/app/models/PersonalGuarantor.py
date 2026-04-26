# PersonalGuarantor (FICO, credit history flags)
from sqlalchemy import Column, Integer, VARCHAR, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class PersonalGuarantor(Base):
    __tablename__ = 'personal_guarantors'
    guarantor_id = Column('guarantor_id', Integer, primary_key=True)
    borrower_id = Column('borrower_id', Integer, ForeignKey('borrowers.borrower_id'))
    first_name = Column('first_name', VARCHAR)
    last_name = Column('last_name', VARCHAR)
    fico_score = Column('fico_score', Integer)
    has_bankruptcy = Column('has_bankruptcy', Boolean)
    has_judgments = Column('has_judgments', Boolean)
    has_liens = Column('has_liens', Boolean)
    ownership_pct = Column('ownership_pct', Float)

    borrower = relationship('Borrower', back_populates='guarantors')

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from app.models.base import Base

class Lender(Base):
    __tablename__ = 'lenders'
    lender_id = Column('lender_id', Integer, primary_key=True)
    lender_name = Column('lender_name', VARCHAR, nullable=False)

    policies = relationship('LenderPolicy', back_populates='lender', cascade='all, delete-orphan')

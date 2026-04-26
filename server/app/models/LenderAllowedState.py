from sqlalchemy import Column, Integer, CHAR, ForeignKey
from app.models.base import Base

class LenderAllowedState(Base):
    __tablename__ = 'lender_allowed_states'
    id = Column('id', Integer, primary_key=True)
    policy_id = Column('policy_id', Integer, ForeignKey('lender_policies.policy_id'), nullable=False)
    state = Column('state', CHAR(2), nullable=False)

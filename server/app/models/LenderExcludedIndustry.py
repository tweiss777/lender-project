from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from app.models.base import Base


class LenderExcludedIndustry(Base):
    __tablename__ = 'lender_excluded_industries'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    policy_id = Column('policy_id', Integer, ForeignKey('lender_policies.policy_id'), nullable=False)
    industry = Column('industry', VARCHAR, nullable=False)

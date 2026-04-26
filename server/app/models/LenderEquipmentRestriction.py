from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from app.models.base import Base

class LenderEquipmentRestriction(Base):
    __tablename__ = 'lender_equipment_restrictions'
    id = Column('id', Integer, primary_key=True)
    policy_id = Column('policy_id', Integer, ForeignKey('lender_policies.policy_id'), nullable=False)
    equipment_type = Column('equipment_type', VARCHAR, nullable=False)

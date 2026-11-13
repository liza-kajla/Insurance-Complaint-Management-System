from sqlalchemy import Column, Integer, String
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String, nullable=True)
    role = Column(String, nullable=True)
    insurance_product = Column(String, nullable=True)
    complaint_text = Column(String, nullable=True)
    complaint_category = Column(String, nullable=True)
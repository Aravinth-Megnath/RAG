from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date
from database.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable= False, index=True)
    check_in = Column(Date,nullable=False)
    check_out = Column(Date,nullable=False)
    room_preference = Column(String(100), nullable=False)

    status = Column(String(20),nullable=False, default="CONFIRMED")

    created_at = Column(DateTime, default=datetime.utcnow,nullable=False)

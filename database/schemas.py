from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field, model_validator

class CreateReservation(BaseModel):
    guest_name: str=Field(...,min_length=2, max_length=100)
    email: EmailStr
    check_in: date
    check_out: date
    room_preference: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("Check-out date must be after check-in date.")
        return self

class ReservationResponse(BaseModel):
    id: int
    guest_name: str
    email: EmailStr
    check_in: date
    check_out: date
    room_preference: str | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
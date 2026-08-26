from sqlalchemy.orm import Session
from database.models import Reservation
from database.schemas import CreateReservation

class ReservationService:
    @staticmethod
    def create_reservation(
        db:Session,
        reservation_data:CreateReservation
        ) -> Reservation:

        reservation = Reservation(
            guest_name=reservation_data.guest_name,
            email=reservation_data.email,
            check_in=reservation_data.check_in,
            check_out=reservation_data.check_out,
            room_preference=reservation_data.room_preference

        )

        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def get_reservation(
        db:Session,
        reservation_id:int,
        email:str
        ) -> Reservation | None:

        reservation = (
            db.query(Reservation).filter(
                Reservation.id == reservation_id,
                Reservation.email == email
            ).first()
        )

        return reservation

    @staticmethod
    def cancel_reservation(
        db: Session,
        reservation_id: int,
        email: str
    )->Reservation | None:

        reservation = (
            db.query(Reservation).filter(
                Reservation.id == reservation_id,
                Reservation.email == email
            ).first()
        )

        if reservation is None:
            return None

        reservation.status = "CANCELLED"

        db.commit()
        db.refresh(reservation)
        return reservation
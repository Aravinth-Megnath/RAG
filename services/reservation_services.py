from sqlalchemy.orm import Session
from database.models import Reservation
from database.schemas import CreateReservation


class ReservationService:
    """Database Access Object (DAO) for handling hotel reservation CRUD operations."""

    @classmethod
    def create_reservation(cls, db: Session, reservation_data: CreateReservation) -> Reservation:
        """Creates a new reservation record in the database."""
        reservation = Reservation(**reservation_data.model_dump())
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation

    @classmethod
    def get_reservation(cls, db: Session, reservation_id: int, email: str) -> Reservation | None:
        """Retrieves a reservation by ID and guest email."""
        return (
            db.query(Reservation)
            .filter(Reservation.id == reservation_id, Reservation.email == email)
            .first()
        )

    @classmethod
    def cancel_reservation(cls, db: Session, reservation_id: int, email: str) -> Reservation | None:
        """Cancels an existing reservation if found."""
        reservation = cls.get_reservation(db, reservation_id, email)
        if not reservation:
            return None

        reservation.status = "CANCELLED"
        db.commit()
        db.refresh(reservation)
        return reservation
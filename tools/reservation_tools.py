from contextlib import contextmanager
from langchain_core.tools import tool
from database.database import session_local
from database.schemas import CreateReservation
from services.reservation_services import ReservationService


@contextmanager
def get_db_session():
    """Context manager to cleanly manage SQLite DB session lifecycle."""
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@tool
def create_reservation(
    guest_name: str,
    email: str,
    check_in: str,
    check_out: str,
    room_preference: str | None = None
) -> dict:
    """
    Create a new hotel reservation.

    Required: guest_name, email, check_in, check_out.
    Optional: room_preference.
    Do not create if any required detail is missing; ask the user instead.
    """
    try:
        reservation_data = CreateReservation(
            guest_name=guest_name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            room_preference=room_preference
        )
        with get_db_session() as db:
            reservation = ReservationService.create_reservation(db, reservation_data)
            return {
                "success": True,
                "reservation_id": reservation.id,
                "status": reservation.status,
                "message": "Reservation created successfully."
            }
    except Exception as e:
        return {"success": False, "message": f"Error creating reservation: {str(e)}"}


@tool
def get_reservation(reservation_id: int, email: str) -> dict:
    """Retrieve a reservation using reservation ID and guest email."""
    try:
        with get_db_session() as db:
            reservation = ReservationService.get_reservation(db, reservation_id, email)
            if not reservation:
                return {"success": False, "message": "Reservation not found."}

            return {
                "success": True,
                "reservation_id": reservation.id,
                "check_in": str(reservation.check_in),
                "check_out": str(reservation.check_out),
                "room_preference": reservation.room_preference,
                "status": reservation.status
            }
    except Exception:
        return {"success": False, "message": "Unable to retrieve reservation."}


@tool
def cancel_reservation(reservation_id: int, email: str) -> dict:
    """Cancel a reservation using reservation ID and guest email."""
    try:
        with get_db_session() as db:
            reservation = ReservationService.cancel_reservation(db, reservation_id, email)
            if not reservation:
                return {"success": False, "message": "Reservation not found or already cancelled."}

            return {
                "success": True,
                "reservation_id": reservation.id,
                "status": reservation.status,
                "message": "Reservation cancelled successfully."
            }
    except Exception:
        return {"success": False, "message": "Unable to cancel reservation."} 
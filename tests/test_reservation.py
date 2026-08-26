from datetime import date

from database.database import session_local
from database.schemas import CreateReservation
from services_reservation.reservation_services import ReservationService


db = session_local()

reservation_data = CreateReservation(
    guest_name="Aravinth",
    email="aravinth.recruiting@gmail.com",
    check_in=date(2026, 9, 10),
    check_out=date(2026, 9, 12),
    room_preference="Deluxe"
)

reservation = ReservationService.create_reservation(
    db,
    reservation_data
)

print("Reservation created!")
print("ID:", reservation.id)
print("Status:", reservation.status)

db.close()

reservation = ReservationService.get_reservation(
    db,
    reservation_id=1,
    email="aravinth.recruiting@gmail.com"
)

if reservation:
    print("Reservation found!")
    print("ID:", reservation.id)
    print("Guest:", reservation.guest_name)
    print("Status:", reservation.status)
else:
    print("Reservation not found")

reservation = ReservationService.get_reservation(
    db,
    reservation_id=1,
    email="wrong@example.com"
)

print(reservation)

reservation = ReservationService.cancel_reservation(
    db,
    reservation_id=1,
    email="aravinth.recruiting@gmail.com"
)

if reservation:
    print("Reservation cancelled!")
    print("Status:", reservation.status)
else:
    print("Reservation not found")
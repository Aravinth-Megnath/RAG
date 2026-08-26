from database.schemas import CreateReservation

reservation = CreateReservation(
    guest_name="Aravinth",
    email="aravinth.recruiting@gmail.com",
    check_in="2026-09-10",
    check_out="2026-09-12",
    room_preference="Deluxe"
)

print(reservation)
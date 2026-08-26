from tools.reservation_tools import create_reservation

result = create_reservation(
    guest_name="Aravinth",
    email="aravinthmegnath@gmail.com",
    check_in="2026-09-10",
    check_out="2026-09-12",
    room_preference="Deluxe"
)

print(result)
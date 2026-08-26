from tools.reservation_tools import cancel_reservation

result = cancel_reservation.invoke({
    "reservation_id": 6,
    "email": "aravinth.@gmail.com"
})

print(result)
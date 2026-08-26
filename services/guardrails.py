class Guardrails:

    @staticmethod
    def validate_query(user_message: str) -> tuple[bool, str | None]:

        message = user_message.lower().strip()

        # Privacy restrictions
        restricted_patterns = [
            "show all bookings",
            "show all reservations",
            "list all bookings",
            "list all reservations",
            "all guest",
            "all customers",
            "all reservations",
            "all bookings",
            "customer emails",
            "guest emails",
        ]

        for pattern in restricted_patterns:
            if pattern in message:
                return (
                    False,
                    "I can't provide access to other guests' "
                    "reservation or personal information."
                )

        return True, None
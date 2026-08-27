class Guardrails:
    RESTRICTED_PATTERNS = (
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
    )

    DENIAL_MESSAGE = "I can't provide access to other guests' reservation or personal information."

    @classmethod
    def validate_query(cls, user_message: str) -> tuple[bool, str | None]:
        """Validates user input against privacy rules to prevent data exposure."""
        msg = user_message.lower().strip()
        if any(pattern in msg for pattern in cls.RESTRICTED_PATTERNS):
            return False, cls.DENIAL_MESSAGE
        return True, None
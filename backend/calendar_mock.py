from datetime import datetime, timedelta, timezone

from logger import get_logger

logger = get_logger("calendar")

# ponytail: hardcoded 5 slots, upgrade to a real calendar API later.
# Slots are naive UTC datetime strings.
_default_slots = [
    (datetime.now(timezone.utc) + timedelta(days=1, hours=10)).isoformat(),
    (datetime.now(timezone.utc) + timedelta(days=1, hours=14)).isoformat(),
    (datetime.now(timezone.utc) + timedelta(days=2, hours=9)).isoformat(),
    (datetime.now(timezone.utc) + timedelta(days=2, hours=13)).isoformat(),
    (datetime.now(timezone.utc) + timedelta(days=3, hours=11)).isoformat(),
]

_booked: dict[str, str] = {}


def book_consultation(name: str, matter_type: str) -> dict:
    """Book the next available slot. Returns booking confirmation."""
    for slot in _default_slots:
        if slot not in _booked:
            _booked[slot] = name
            logger.info("Booked consultation for %s at %s", name, slot)
            return {
                "booked": True,
                "date": slot,
                "matter_type": matter_type,
                "client_name": name,
            }
    return {"booked": False, "reason": "No available slots"}

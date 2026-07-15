"""Milestone 2: query seats.aero Partner API for award availability.

See project spec §4.2. Wraps the seats.aero API for cross-program award
search (origin, destination, flexible date range, cabin, carrier filter).
"""

from datetime import date

from awardhawk.models import AwardResult, Cabin

SEATS_AERO_BASE_URL = "https://seats.aero/partnerapi"


def search_award_availability(
    origin: str,
    destination: str,
    start_date: date,
    end_date: date,
    cabins: list[Cabin],
) -> list[AwardResult]:
    """Query seats.aero for award availability across relevant programs."""
    raise NotImplementedError

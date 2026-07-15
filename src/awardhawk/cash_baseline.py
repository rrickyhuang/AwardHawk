"""Milestone 4: fetch a comparable cash fare baseline for CPP calculation.

See project spec §4.4. Candidate source is the Amadeus Self-Service flight
search API; an approximate fare is acceptable for v1.
"""

from datetime import date

from awardhawk.models import Cabin, CashFareEstimate


def get_cash_fare_estimate(
    origin: str, destination: str, travel_date: date, cabin: Cabin
) -> CashFareEstimate:
    """Return an approximate cash fare estimate for the given route/date/cabin."""
    raise NotImplementedError

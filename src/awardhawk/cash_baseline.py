"""Milestone 4: fetch a comparable cash fare baseline for CPP calculation.

See project spec §4.4. Uses the Amadeus Self-Service Flight Offers Search
API (test/free tier) — chosen over an MCP flight-search connector because
this pipeline runs unattended via Windows Task Scheduler (see #10, #11),
outside any Claude session (spec §7, decided in GitHub issue #6). An
approximate fare is acceptable for v1; premium-cabin coverage is expected
to be sparse.
"""

import os
from datetime import date

import requests

from awardhawk.models import Cabin, CashFareEstimate

_TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
_OFFERS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

_CABIN_MAP = {
    Cabin.ECONOMY: "ECONOMY",
    Cabin.PREMIUM_ECONOMY: "PREMIUM_ECONOMY",
    Cabin.BUSINESS: "BUSINESS",
    Cabin.FIRST: "FIRST",
}


def _get_access_token() -> str:
    """Fetch a client-credentials access token from Amadeus."""
    client_id = os.environ["AMADEUS_CLIENT_ID"]
    client_secret = os.environ["AMADEUS_CLIENT_SECRET"]

    response = requests.post(
        _TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def _fetch_flight_offers(
    origin: str, destination: str, travel_date: date, cabin: Cabin, access_token: str
) -> dict:
    """Query the Amadeus Flight Offers Search API for a single route/date/cabin."""
    response = requests.get(
        _OFFERS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": travel_date.isoformat(),
            "adults": 1,
            "travelClass": _CABIN_MAP[cabin],
            "currencyCode": "CAD",
            "max": 10,
            "nonStop": "false",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _parse_cheapest_offer(
    response_json: dict, origin: str, destination: str, travel_date: date, cabin: Cabin
) -> CashFareEstimate:
    """Pick the lowest-priced offer out of an Amadeus flight-offers response."""
    offers = response_json.get("data") or []
    if not offers:
        raise ValueError(
            f"No Amadeus flight offers found for {origin}->{destination} "
            f"on {travel_date} ({cabin.value})"
        )

    cheapest = min(offers, key=lambda offer: float(offer["price"]["total"]))
    price = cheapest["price"]

    return CashFareEstimate(
        origin=origin,
        destination=destination,
        date=travel_date,
        cabin=cabin,
        fare_amount=float(price["total"]),
        currency=price["currency"],
    )


def get_cash_fare_estimate(
    origin: str, destination: str, travel_date: date, cabin: Cabin
) -> CashFareEstimate:
    """Return an approximate cash fare estimate for the given route/date/cabin."""
    access_token = _get_access_token()
    response_json = _fetch_flight_offers(origin, destination, travel_date, cabin, access_token)
    return _parse_cheapest_offer(response_json, origin, destination, travel_date, cabin)

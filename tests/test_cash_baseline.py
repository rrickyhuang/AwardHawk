import json
from datetime import date
from pathlib import Path

import pytest

from awardhawk import cash_baseline
from awardhawk.models import Cabin

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "amadeus_flight_offers_sample.json"


def _sample_offers() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_parse_cheapest_offer_picks_lowest_price():
    estimate = cash_baseline._parse_cheapest_offer(
        _sample_offers(), "YVR", "SIN", date(2026, 9, 22), Cabin.BUSINESS
    )

    assert estimate.fare_amount == 2050.75
    assert estimate.currency == "CAD"
    assert estimate.origin == "YVR"
    assert estimate.destination == "SIN"
    assert estimate.cabin == Cabin.BUSINESS


def test_parse_cheapest_offer_raises_on_no_offers():
    with pytest.raises(ValueError):
        cash_baseline._parse_cheapest_offer(
            {"data": []}, "YVR", "SIN", date(2026, 9, 22), Cabin.BUSINESS
        )


def test_get_access_token_reads_env_and_posts(monkeypatch):
    monkeypatch.setenv("AMADEUS_CLIENT_ID", "id123")
    monkeypatch.setenv("AMADEUS_CLIENT_SECRET", "secret456")

    captured = {}

    class _FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"access_token": "fake-token"}

    def _fake_post(url, data=None, timeout=None):
        captured["url"] = url
        captured["data"] = data
        return _FakeResponse()

    monkeypatch.setattr(cash_baseline.requests, "post", _fake_post)

    token = cash_baseline._get_access_token()

    assert token == "fake-token"
    assert captured["data"]["client_id"] == "id123"
    assert captured["data"]["client_secret"] == "secret456"
    assert captured["url"] == cash_baseline._TOKEN_URL


def test_get_cash_fare_estimate_end_to_end(monkeypatch):
    monkeypatch.setenv("AMADEUS_CLIENT_ID", "id123")
    monkeypatch.setenv("AMADEUS_CLIENT_SECRET", "secret456")

    class _FakeTokenResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"access_token": "fake-token"}

    class _FakeOffersResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return _sample_offers()

    monkeypatch.setattr(cash_baseline.requests, "post", lambda *a, **k: _FakeTokenResponse())
    monkeypatch.setattr(cash_baseline.requests, "get", lambda *a, **k: _FakeOffersResponse())

    estimate = cash_baseline.get_cash_fare_estimate(
        "YVR", "SIN", date(2026, 9, 22), Cabin.BUSINESS
    )

    assert estimate.fare_amount == 2050.75
    assert estimate.currency == "CAD"

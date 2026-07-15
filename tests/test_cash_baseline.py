from datetime import date

import pytest

from awardhawk import cash_baseline
from awardhawk.models import Cabin


def test_get_cash_fare_estimate_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        cash_baseline.get_cash_fare_estimate("YVR", "SIN", date(2026, 9, 22), Cabin.BUSINESS)

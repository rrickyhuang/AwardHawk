from datetime import date

import pytest

from awardhawk import award_search
from awardhawk.models import Cabin


def test_search_award_availability_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        award_search.search_award_availability(
            "YVR", "SIN", date(2026, 9, 22), date(2026, 10, 22), [Cabin.BUSINESS]
        )

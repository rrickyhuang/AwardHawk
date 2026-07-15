import pytest

from awardhawk import bonus_monitor


def test_parse_bonuses_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        bonus_monitor.parse_bonuses("<table></table>")

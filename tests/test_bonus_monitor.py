from datetime import date
from pathlib import Path

from awardhawk import bonus_monitor

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "frequentmiler_sample.html"


def _sample_html() -> str:
    return FIXTURE_PATH.read_text(encoding="utf-8")


def test_parse_bonuses_filters_to_amex_mr():
    bonuses = bonus_monitor.parse_bonuses(_sample_html())

    # Only the two Amex MR rows should survive; the Citi row is filtered out.
    assert len(bonuses) == 2
    assert {b.from_program for b in bonuses} == {"Amex Membership Rewards"}
    assert {b.to_program for b in bonuses} == {"Avianca LifeMiles", "Virgin Atlantic Flying Club"}


def test_parse_bonuses_extracts_fields():
    bonuses = bonus_monitor.parse_bonuses(_sample_html())
    avianca = next(b for b in bonuses if b.to_program == "Avianca LifeMiles")

    assert avianca.bonus_percent == 0.15
    assert avianca.start_date == date(2026, 6, 15)
    assert avianca.end_date == date(2026, 7, 15)
    assert avianca.source_url.startswith("https://frequentmiler.com/")
    assert avianca.targeted is False


def test_diff_against_seen_first_run_returns_all(tmp_path):
    bonuses = bonus_monitor.parse_bonuses(_sample_html())
    seen_path = tmp_path / "seen_bonuses.json"

    changed = bonus_monitor.diff_against_seen(bonuses, str(seen_path))

    assert len(changed) == len(bonuses)
    assert seen_path.exists()


def test_diff_against_seen_second_run_returns_nothing_new(tmp_path):
    bonuses = bonus_monitor.parse_bonuses(_sample_html())
    seen_path = tmp_path / "seen_bonuses.json"

    bonus_monitor.diff_against_seen(bonuses, str(seen_path))
    changed = bonus_monitor.diff_against_seen(bonuses, str(seen_path))

    assert changed == []


def test_diff_against_seen_detects_new_bonus(tmp_path):
    bonuses = bonus_monitor.parse_bonuses(_sample_html())
    seen_path = tmp_path / "seen_bonuses.json"

    bonus_monitor.diff_against_seen(bonuses[:1], str(seen_path))
    changed = bonus_monitor.diff_against_seen(bonuses, str(seen_path))

    assert len(changed) == 1
    assert changed[0].to_program == bonuses[1].to_program

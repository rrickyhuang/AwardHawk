"""Milestone 1: scrape and diff Amex transfer bonuses from frequentmiler.com.

See project spec §4.3. Fetches the "Current point transfer bonuses" table,
parses rows, filters to Amex Membership Rewards as the "Transfer From" column,
and diffs against a local seen-rows store to surface new/changed bonuses.
"""

from awardhawk.models import TransferBonus

FREQUENTMILER_URL = "https://frequentmiler.com/current-transfer-bonuses/"


def fetch_bonus_table_html() -> str:
    """Fetch the raw HTML of the frequentmiler transfer bonus table."""
    raise NotImplementedError


def parse_bonuses(html: str) -> list[TransferBonus]:
    """Parse the bonus table HTML into TransferBonus rows, filtered to Amex MR."""
    raise NotImplementedError


def diff_against_seen(current: list[TransferBonus], seen_path: str) -> list[TransferBonus]:
    """Return bonuses in `current` that are new or changed vs. the local seen store."""
    raise NotImplementedError

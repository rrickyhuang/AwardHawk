"""Milestone 1: scrape and diff Amex transfer bonuses from frequentmiler.com.

See project spec §4.3. Fetches the "Current and Upcoming Transfer Bonuses"
table, parses rows, filters to Amex Membership Rewards as the "Transfer
From" column, and diffs against a local seen-rows store to surface
new/changed bonuses.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from awardhawk.models import TransferBonus

FREQUENTMILER_URL = "https://frequentmiler.com/current-point-transfer-bonuses/"

# "Transfer Bonus Details" cell text looks like:
#   "15% transfer bonus from Amex Membership Rewards to Avianca LifeMiles"
_DETAIL_RE = re.compile(r"^\s*([\d.]+)%\s+transfer bonus from .+? to (.+?)\s*$", re.IGNORECASE)

_AMEX_MR = "Amex Membership Rewards"

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AwardHawk/0.1"}


def fetch_bonus_table_html() -> str:
    """Fetch the raw HTML of the frequentmiler transfer bonus page."""
    response = requests.get(FREQUENTMILER_URL, headers=_HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def _parse_date_cell(cell) -> "datetime.date":
    # Each date cell contains a hidden <p> with an Excel-style serial number
    # (used by the table's JS sort) followed by the visible MM/DD/YY text.
    hidden = cell.find("p")
    if hidden is not None:
        hidden.decompose()
    text = cell.get_text(strip=True)
    return datetime.strptime(text, "%m/%d/%y").date()


def parse_bonuses(html: str) -> list[TransferBonus]:
    """Parse the bonus table HTML into TransferBonus rows, filtered to Amex MR."""
    soup = BeautifulSoup(html, "html.parser")

    table = None
    for candidate in soup.find_all("table"):
        header_text = candidate.get_text(" ", strip=True)
        if "Transfer From" in header_text and "Transfer Bonus Details" in header_text:
            table = candidate
            break
    if table is None:
        return []

    body = table.find("tbody") or table
    bonuses: list[TransferBonus] = []

    for row in body.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        from_program = cells[0].get_text(strip=True)
        if from_program != _AMEX_MR:
            continue

        detail_link = cells[1].find("a")
        detail_text = (detail_link or cells[1]).get_text(strip=True)
        source_url = detail_link["href"] if detail_link else ""

        match = _DETAIL_RE.match(detail_text)
        if not match:
            continue
        bonus_percent = float(match.group(1)) / 100
        to_program = match.group(2).strip()

        start_date = _parse_date_cell(cells[2])
        end_date = _parse_date_cell(cells[3])

        # Targeted (YMMV) offers aren't distinguishable from this table alone;
        # default False, but this can't be auto-verified (spec §4.3, §7).
        bonuses.append(
            TransferBonus(
                from_program=from_program,
                to_program=to_program,
                bonus_percent=bonus_percent,
                start_date=start_date,
                end_date=end_date,
                source_url=source_url,
                targeted=False,
            )
        )

    return bonuses


def diff_against_seen(current: list[TransferBonus], seen_path: str) -> list[TransferBonus]:
    """Return bonuses in `current` that are new or changed vs. the local seen store.

    Bonuses are keyed by source_url. The store at `seen_path` is overwritten
    with the full current state after diffing.
    """
    path = Path(seen_path)
    previous: dict[str, dict] = {}
    if path.exists():
        previous = json.loads(path.read_text(encoding="utf-8"))

    changed: list[TransferBonus] = []
    current_by_url: dict[str, dict] = {}
    for bonus in current:
        dumped = bonus.model_dump(mode="json")
        current_by_url[bonus.source_url] = dumped
        if previous.get(bonus.source_url) != dumped:
            changed.append(bonus)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(current_by_url, indent=2), encoding="utf-8")

    return changed

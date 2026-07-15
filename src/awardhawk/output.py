"""Milestone 5: render ranked options as an HTML digest.

See project spec §4.6. Reuses the delivery pattern from the existing
theatre-watchlist checker: a single ranked table (Program | Dates | Cabin |
Miles Required | Active Bonus | Effective Amex Points | Cash Baseline | CPP | Notes).
"""

from awardhawk.models import RankedOption


def render_html_digest(options: list[RankedOption]) -> str:
    """Render ranked options as an HTML digest table."""
    raise NotImplementedError

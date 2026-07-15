"""Milestone 3/4: join award results, bonuses, and cash baselines into ranked CPP options.

See project spec §4.5.

    effective_amex_points = miles_required / (1 + bonus_percent)
    cpp = (cash_fare_estimate - award_taxes_and_fees) / effective_amex_points * 100

Pre-funded no-transfer programs (see config.NO_TRANSFER_PROGRAMS) skip the
bonus/transfer step and are flagged in notes instead of excluded.
"""

from awardhawk.models import AwardResult, CashFareEstimate, RankedOption, TransferBonus


def compute_ranked_option(
    award: AwardResult,
    bonus: TransferBonus | None,
    cash_baseline: CashFareEstimate,
    award_taxes_and_fees: float,
) -> RankedOption:
    """Compute effective points and CPP for a single award result."""
    raise NotImplementedError


def rank_options(options: list[RankedOption]) -> list[RankedOption]:
    """Sort ranked options by CPP, descending."""
    raise NotImplementedError

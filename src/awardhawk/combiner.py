"""Milestone 4: join award results, bonuses, and cash baselines into ranked CPP options.

See project spec §4.5.

    effective_amex_points = miles_required / (1 + bonus_percent)
    cpp = (cash_fare_estimate - award_taxes_and_fees) / effective_amex_points * 100

Pre-funded no-transfer programs (see config.NO_TRANSFER_PROGRAMS) skip the
bonus/transfer step and are flagged in notes instead of excluded.
"""

from awardhawk import config
from awardhawk.models import AwardResult, CashFareEstimate, RankedOption, TransferBonus


def compute_ranked_option(
    award: AwardResult,
    bonus: TransferBonus | None,
    cash_baseline: CashFareEstimate,
    award_taxes_and_fees: float,
) -> RankedOption:
    """Compute effective points and CPP for a single award result."""
    notes: list[str] = []

    if award.program in config.NO_TRANSFER_PROGRAMS:
        effective_points = award.miles_required
        excise_tax = 0.0
        notes.append("no transfer needed")
    else:
        if bonus is not None:
            effective_points = round(award.miles_required / (1 + bonus.bonus_percent))
            notes.append(f"{bonus.bonus_percent:.0%} transfer bonus applied")
        else:
            effective_points = award.miles_required
        excise_tax = effective_points * config.AMEX_EXCISE_TAX_PER_POINT

    cpp = (
        (cash_baseline.fare_amount - award_taxes_and_fees - excise_tax)
        / effective_points
        * 100
    )

    return RankedOption(
        award_result=award,
        applicable_bonus=bonus,
        effective_amex_points=effective_points,
        cash_baseline=cash_baseline,
        cpp=cpp,
        notes=notes,
    )


def rank_options(options: list[RankedOption]) -> list[RankedOption]:
    """Sort ranked options by CPP, descending (highest value per point = best)."""
    return sorted(options, key=lambda option: option.cpp, reverse=True)

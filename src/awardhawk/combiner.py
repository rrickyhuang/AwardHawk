"""Milestone 3/4: join award results, bonuses, and cash baselines into ranked CPP options.

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
        notes.append("no transfer needed")
    elif bonus is not None:
        effective_points = round(award.miles_required / (1 + bonus.bonus_percent))
        notes.append(f"{bonus.bonus_percent:.0%} transfer bonus applied")
    else:
        effective_points = award.miles_required

    cpp = (cash_baseline.fare_amount - award_taxes_and_fees) / effective_points * 100

    return RankedOption(
        award_result=award,
        applicable_bonus=bonus,
        effective_amex_points=effective_points,
        cash_baseline=cash_baseline,
        cpp=cpp,
        notes=notes,
    )


def rank_options(options: list[RankedOption]) -> list[RankedOption]:
    """Sort ranked options by effective Amex points, ascending (fewest points = best).

    Miles-only ranking for milestone 3; CPP isn't factored in until the cash
    baseline lands (#8), which re-ranks by CPP descending instead.
    """
    return sorted(options, key=lambda option: option.effective_amex_points)

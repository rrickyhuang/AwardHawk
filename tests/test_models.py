from datetime import date

from awardhawk.models import AwardResult, Cabin, CashFareEstimate, RankedOption, TransferBonus


def test_award_result_construction():
    result = AwardResult(
        program="Aeroplan",
        origin="YVR",
        destination="SIN",
        date=date(2026, 9, 22),
        cabin=Cabin.BUSINESS,
        miles_required=87500,
        seats_available=2,
        routing="YVR-NRT-SIN",
    )
    assert result.program == "Aeroplan"


def test_ranked_option_allows_no_bonus():
    award = AwardResult(
        program="Aeroplan",
        origin="YVR",
        destination="SIN",
        date=date(2026, 9, 22),
        cabin=Cabin.BUSINESS,
        miles_required=87500,
        seats_available=2,
        routing="YVR-NRT-SIN",
    )
    cash = CashFareEstimate(
        origin="YVR", destination="SIN", date=date(2026, 9, 22), cabin=Cabin.BUSINESS,
        fare_amount=4200.0, currency="CAD",
    )
    option = RankedOption(
        award_result=award,
        applicable_bonus=None,
        effective_amex_points=87500,
        cash_baseline=cash,
        cpp=4.5,
        notes=["no transfer needed - Aeroplan balance"],
    )
    assert option.applicable_bonus is None

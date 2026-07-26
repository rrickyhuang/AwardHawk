from datetime import date

from awardhawk import combiner
from awardhawk.models import AwardResult, Cabin, CashFareEstimate, TransferBonus

_CASH = CashFareEstimate(
    origin="YVR", destination="SIN", date=date(2026, 9, 22), cabin=Cabin.BUSINESS,
    fare_amount=4200.0, currency="CAD",
)


def _award(program: str, miles: int) -> AwardResult:
    return AwardResult(
        program=program,
        origin="YVR",
        destination="SIN",
        date=date(2026, 9, 22),
        cabin=Cabin.BUSINESS,
        miles_required=miles,
        seats_available=2,
        routing="YVR-NRT-SIN",
    )


def _bonus(to_program: str, percent: float) -> TransferBonus:
    return TransferBonus(
        from_program="Amex Membership Rewards",
        to_program=to_program,
        bonus_percent=percent,
        start_date=date(2026, 6, 15),
        end_date=date(2026, 7, 15),
        source_url="https://frequentmiler.com/example",
        targeted=False,
    )


def test_compute_ranked_option_no_transfer_program_skips_bonus():
    award = _award("Aeroplan", 87500)

    option = combiner.compute_ranked_option(award, None, _CASH, 100.0)

    assert option.effective_amex_points == 87500
    assert "no transfer needed" in option.notes


def test_compute_ranked_option_applies_bonus():
    award = _award("Avianca LifeMiles", 115000)
    bonus = _bonus("Avianca LifeMiles", 0.15)

    option = combiner.compute_ranked_option(award, bonus, _CASH, 100.0)

    assert option.effective_amex_points == round(115000 / 1.15)
    assert option.applicable_bonus is bonus
    assert any("transfer bonus applied" in note for note in option.notes)


def test_compute_ranked_option_no_bonus_uses_raw_miles():
    award = _award("ANA Mileage Club", 90000)

    option = combiner.compute_ranked_option(award, None, _CASH, 100.0)

    assert option.effective_amex_points == 90000
    assert option.notes == []


def test_compute_ranked_option_computes_cpp():
    award = _award("Aeroplan", 87500)

    option = combiner.compute_ranked_option(award, None, _CASH, 100.0)

    assert option.cpp == (4200.0 - 100.0) / 87500 * 100


def test_compute_ranked_option_deducts_excise_tax_on_transfer():
    award = _award("ANA Mileage Club", 90000)

    option = combiner.compute_ranked_option(award, None, _CASH, 100.0)

    excise_tax = 90000 * combiner.config.AMEX_EXCISE_TAX_PER_POINT
    assert option.cpp == (4200.0 - 100.0 - excise_tax) / 90000 * 100


def test_compute_ranked_option_no_excise_tax_for_no_transfer_program():
    award = _award("Aeroplan", 87500)

    option = combiner.compute_ranked_option(award, None, _CASH, 100.0)

    assert option.cpp == (4200.0 - 100.0) / 87500 * 100


def test_rank_options_sorts_by_cpp_descending():
    better = combiner.compute_ranked_option(_award("Aeroplan", 60000), None, _CASH, 100.0)
    worse = combiner.compute_ranked_option(_award("ANA Mileage Club", 90000), None, _CASH, 100.0)

    ranked = combiner.rank_options([worse, better])

    assert ranked == [better, worse]

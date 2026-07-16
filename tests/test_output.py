from datetime import date

from awardhawk import output
from awardhawk.models import AwardResult, Cabin, CashFareEstimate, RankedOption, TransferBonus


def _option(with_bonus: bool = True) -> RankedOption:
    award = AwardResult(
        program="Avianca LifeMiles",
        origin="YVR",
        destination="SIN",
        date=date(2026, 9, 22),
        cabin=Cabin.BUSINESS,
        miles_required=115000,
        seats_available=2,
        routing="YVR-NRT-SIN",
    )
    bonus = TransferBonus(
        from_program="Amex Membership Rewards",
        to_program="Avianca LifeMiles",
        bonus_percent=0.15,
        start_date=date(2026, 6, 15),
        end_date=date(2026, 7, 15),
        source_url="https://frequentmiler.com/example",
        targeted=False,
    ) if with_bonus else None
    cash = CashFareEstimate(
        origin="YVR", destination="SIN", date=date(2026, 9, 22), cabin=Cabin.BUSINESS,
        fare_amount=4200.0, currency="CAD",
    )
    return RankedOption(
        award_result=award,
        applicable_bonus=bonus,
        effective_amex_points=100000,
        cash_baseline=cash,
        cpp=4.1,
        notes=["15% transfer bonus applied"] if with_bonus else [],
    )


def test_render_html_digest_empty():
    html = output.render_html_digest([])

    assert "No ranked options" in html


def test_render_html_digest_includes_option_fields():
    html = output.render_html_digest([_option()])

    assert "Avianca LifeMiles" in html
    assert "2026-09-22" in html
    assert "115,000" in html
    assert "100,000" in html
    assert "4,200.00 CAD" in html
    assert "4.10¢" in html
    assert "15% transfer bonus applied" in html


def test_render_html_digest_escapes_untrusted_text():
    option = _option(with_bonus=False)
    option.notes.append('<script>alert("x")</script>')

    html = output.render_html_digest([option])

    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_render_html_digest_no_bonus_shows_placeholder():
    html = output.render_html_digest([_option(with_bonus=False)])

    assert 'class="no-bonus"' in html

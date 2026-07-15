# AwardHawk

Points & miles award deal finder. Combines live award seat availability, Amex
Membership Rewards transfer bonuses, and a cash-fare baseline into a single
ranked view of cents-per-point (CPP) value for a given route and date range.

## Problem

Finding good award redemptions requires manually correlating three things
that live in separate places: award seat availability, time-limited transfer
bonuses, and a cash-fare baseline to judge value. AwardHawk automates that
correlation.

## v1 scope

- Route: YVR (Vancouver) → SIN (Singapore), flexible dates from 2026-09-22.
- Points source: Amex Membership Rewards → Star Alliance programs (Aeroplan,
  ANA Mileage Club, Avianca LifeMiles). Aeroplan is a pre-funded balance and
  is flagged distinctly (no transfer needed).
- Output only — no booking, no point-balance tracking, no hotel transfers.

## Architecture

```
[Bonus Monitor] ─┐
                  ├─→ [Combiner / CPP Calculator] ─→ [Ranked Output]
[Award Search]   ─┤
                  │
[Cash Baseline]  ─┘
```

- **Bonus Monitor** (`awardhawk/bonus_monitor.py`) — scrapes and diffs Amex
  transfer bonuses from frequentmiler.com.
- **Award Search** (`awardhawk/award_search.py`) — queries the seats.aero
  Partner API for cross-program award availability.
- **Cash Baseline** (`awardhawk/cash_baseline.py`) — fetches an approximate
  cash fare for the same route/date/cabin (Amadeus Self-Service API).
- **Combiner** (`awardhawk/combiner.py`) — joins the above and computes CPP.
- **Output** (`awardhawk/output.py`) — renders a ranked HTML digest.

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
copy .env.example .env   # fill in SEATS_AERO_API_KEY, AMADEUS_CLIENT_ID/SECRET
```

## Running

```
pytest                       # run tests
python scripts/run_daily.py  # full pipeline (scheduled entrypoint)
```

## Status

Milestone 0 (scaffold) complete. See `CLAUDE.md` for the milestone tracker
and full project spec.

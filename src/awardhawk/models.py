from datetime import date
from enum import Enum

from pydantic import BaseModel


class Cabin(str, Enum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class AwardResult(BaseModel):
    program: str
    origin: str
    destination: str
    date: date
    cabin: Cabin
    miles_required: int
    seats_available: int
    routing: str


class TransferBonus(BaseModel):
    from_program: str
    to_program: str
    bonus_percent: float
    start_date: date
    end_date: date
    source_url: str
    targeted: bool


class CashFareEstimate(BaseModel):
    origin: str
    destination: str
    date: date
    cabin: Cabin
    fare_amount: float
    currency: str


class RankedOption(BaseModel):
    award_result: AwardResult
    applicable_bonus: TransferBonus | None
    effective_amex_points: int
    cash_baseline: CashFareEstimate
    cpp: float
    notes: list[str]

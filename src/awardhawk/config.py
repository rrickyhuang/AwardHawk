"""v1 use-case config: YVR -> SIN, flexible dates, Amex-transferable Star Alliance programs."""

from datetime import date

ORIGIN = "YVR"
DESTINATION = "SIN"
FLEX_START_DATE = date(2026, 9, 22)

# Amex Membership Rewards transfer partners relevant to this route (Star Alliance / SIN-serving).
RELEVANT_PROGRAMS = [
    "Aeroplan",
    "ANA Mileage Club",
    "Avianca LifeMiles",
]

# Aeroplan is a pre-funded, no-transfer-needed balance for v1 and should be flagged
# distinctly in output rather than run through the bonus/transfer calculation path.
NO_TRANSFER_PROGRAMS = ["Aeroplan"]

TARGET_CABINS = ["economy", "business"]

# Amex -> foreign airline program excise tax, ~0.06 cents/point, capped (spec §7).
AMEX_EXCISE_TAX_PER_POINT = 0.0006

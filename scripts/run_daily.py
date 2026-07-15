"""Milestone 5: scheduled entrypoint (e.g. Windows Task Scheduler target).

Runs the full pipeline: bonus monitor -> award search -> cash baseline ->
combiner -> output digest. Degrades gracefully per spec §6: if the cash
baseline step fails, fall back to a miles-only ranking rather than blocking
the whole run.
"""


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()

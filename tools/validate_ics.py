#!/usr/bin/env python3
"""
validate_ics.py — Validate generated .ics calendars.

Part of the Pyros World Events Calendar (WAT framework, tools layer).

Checks each .ics file in calendars/ (or paths given on the CLI) for:
  - Parses as a valid VCALENDAR with VERSION + PRODID.
  - Has >= 1 VEVENT.
  - Every VEVENT has UID, DTSTART, SUMMARY.
  - UIDs are unique within the calendar.
  - Timed events carry timezone info (no naive datetimes).
  - Not "past-only": at least one event is today or in the future (else warn —
    a calendar of only past events is almost always stale).

Exit code is non-zero if any ERROR-level check fails (WARN does not fail).

Usage:
    python tools/validate_ics.py
    python tools/validate_ics.py calendars/shopping-events.ics
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timezone
from pathlib import Path

from icalendar import Calendar

ROOT = Path(__file__).resolve().parent.parent
CAL_DIR = ROOT / "calendars"


def _as_date(dt) -> date:
    if isinstance(dt, datetime):
        return dt.date()
    return dt


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    try:
        cal = Calendar.from_ical(path.read_bytes())
    except Exception as exc:  # noqa: BLE001
        return [f"failed to parse: {exc}"], warns

    if not cal.get("version"):
        errors.append("missing VERSION")
    if not cal.get("prodid"):
        warns.append("missing PRODID")

    events = [c for c in cal.walk("VEVENT")]
    if not events:
        errors.append("no VEVENT components")
        return errors, warns

    seen_uids: set[str] = set()
    today = date.today()
    has_future = False

    for i, ev in enumerate(events):
        label = str(ev.get("summary", f"event #{i}"))
        uid = ev.get("uid")
        if not uid:
            errors.append(f"{label}: missing UID")
        else:
            uid = str(uid)
            if uid in seen_uids:
                errors.append(f"duplicate UID: {uid}")
            seen_uids.add(uid)
        if not ev.get("summary"):
            errors.append(f"event #{i}: missing SUMMARY")

        dtstart = ev.get("dtstart")
        if dtstart is None:
            errors.append(f"{label}: missing DTSTART")
            continue
        val = dtstart.dt
        if isinstance(val, datetime) and val.tzinfo is None:
            errors.append(f"{label}: timed event has naive datetime (no timezone)")
        if _as_date(val) >= today:
            has_future = True

    if not has_future:
        warns.append("all events are in the past — calendar looks stale")

    return errors, warns


def main() -> int:
    args = sys.argv[1:]
    if args:
        paths = [Path(a) for a in args]
    else:
        paths = sorted(CAL_DIR.glob("*.ics"))

    if not paths:
        print("No .ics files found to validate.", file=sys.stderr)
        return 1

    total_errors = 0
    for path in paths:
        errors, warns = validate_file(path)
        status = "FAIL" if errors else ("WARN" if warns else "PASS")
        print(f"[{status}] {path.name}")
        for e in errors:
            print(f"    ERROR: {e}")
        for w in warns:
            print(f"    warn:  {w}")
        total_errors += len(errors)

    print(f"\n{len(paths)} file(s) checked, {total_errors} error(s).")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

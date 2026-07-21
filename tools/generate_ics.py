#!/usr/bin/env python3
"""
generate_ics.py — Build category .ics calendars from data/events.yaml.

Part of the Pyros World Events Calendar (WAT framework, tools layer).

Reads the human-reviewable single source of truth (data/events.yaml) and emits
one RFC-5545 .ics file per calendar into calendars/. These are the CUSTOM /
curated calendars (tentpole events). Official auto-updating feeds are subscribed
directly and are NOT generated here (see data/feeds_registry.yaml).

Design rules (see SPEC.md):
  - All-day events use DATE values (no time). Multi-day all-day events set an
    EXCLUSIVE DTEND per RFC 5545 (last day + 1).
  - Timed events are stored with an explicit IANA timezone; icalendar emits the
    matching VTIMEZONE automatically.
  - UIDs are STABLE (derived from calendar id + event slug + start) so that
    re-running the generator updates events in place instead of duplicating them.
  - Every event should carry source_url + last_verified (enforced by validator).

Usage:
    python tools/generate_ics.py                # generate all calendars
    python tools/generate_ics.py --only shopping-events holidays-awareness
    python tools/generate_ics.py --check        # parse-only, don't write
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from icalendar import Calendar, Event

ROOT = Path(__file__).resolve().parent.parent
EVENTS_FILE = ROOT / "data" / "events.yaml"
OUT_DIR = ROOT / "calendars"

UID_DOMAIN = "pyros-world-events-calendar"


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def parse_when(value):
    """Return (python date|datetime, is_all_day). Accepts 'YYYY-MM-DD' (all-day)
    or ISO 'YYYY-MM-DDTHH:MM[:SS]' (timed)."""
    if isinstance(value, datetime):
        return value, False
    if isinstance(value, date):
        return value, True
    s = str(value).strip()
    if "T" in s:
        return datetime.fromisoformat(s), False
    return date.fromisoformat(s), True


def build_event(cal_id: str, raw: dict) -> Event:
    if "summary" not in raw or "start" not in raw:
        raise ValueError(f"[{cal_id}] event missing required 'summary'/'start': {raw!r}")

    ev = Event()
    summary = str(raw["summary"]).strip()
    start, all_day = parse_when(raw["start"])

    # Stable UID so re-generation updates rather than duplicates.
    start_key = start.date().isoformat() if isinstance(start, datetime) else start.isoformat()
    uid = raw.get("uid") or f"{slugify(summary)}-{start_key}@{cal_id}.{UID_DOMAIN}"
    ev.add("uid", uid)
    ev.add("summary", summary)

    if all_day:
        ev.add("dtstart", start)
        # DTEND is exclusive for all-day events. 'end' in YAML is the INCLUSIVE
        # last day; add one day. Default: single-day event.
        if raw.get("end"):
            end, _ = parse_when(raw["end"])
            end = end if isinstance(end, date) else end.date()
        else:
            end = start
        ev.add("dtend", end + timedelta(days=1))
    else:
        tz = ZoneInfo(raw.get("tz", "UTC"))
        if start.tzinfo is None:
            start = start.replace(tzinfo=tz)
        ev.add("dtstart", start)
        if raw.get("end"):
            end, _ = parse_when(raw["end"])
            if isinstance(end, datetime) and end.tzinfo is None:
                end = end.replace(tzinfo=tz)
            ev.add("dtend", end)
        else:
            ev.add("dtend", start + timedelta(hours=1))

    # Description carries provenance so it's visible inside the calendar app.
    desc_parts = []
    if raw.get("notes"):
        desc_parts.append(str(raw["notes"]))
    if raw.get("source_url"):
        desc_parts.append(f"Source: {raw['source_url']}")
    if raw.get("last_verified"):
        desc_parts.append(f"Verified: {raw['last_verified']}")
    if desc_parts:
        ev.add("description", "\n".join(desc_parts))
    if raw.get("url") or raw.get("source_url"):
        ev.add("url", raw.get("url") or raw["source_url"])
    ev.add("transp", "TRANSPARENT")  # don't block time; these are informational

    # DTSTAMP: use last_verified if present for deterministic output, else start.
    stamp = raw.get("last_verified")
    try:
        stamp_dt = datetime.fromisoformat(str(stamp)) if stamp else None
    except ValueError:
        stamp_dt = None
    ev.add("dtstamp", stamp_dt or datetime(2026, 1, 1))
    return ev


def build_calendar(cal: dict) -> tuple[str, Calendar]:
    cal_id = cal["id"]
    c = Calendar()
    c.add("prodid", f"-//Pyros//World Events Calendar//{cal_id}//EN")
    c.add("version", "2.0")
    c.add("calscale", "GREGORIAN")
    c.add("method", "PUBLISH")
    c.add("x-wr-calname", cal.get("name", cal_id))
    c.add("x-wr-timezone", "UTC")
    if cal.get("description"):
        c.add("x-wr-caldesc", cal["description"])

    events = cal.get("events") or []
    for raw in events:
        c.add_component(build_event(cal_id, raw))

    # Emit a VTIMEZONE for every TZID referenced by timed events, so the file is
    # valid RFC 5545 and portable to strict clients (Apple Calendar etc.).
    c.add_missing_timezones()
    return cal_id, c


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate .ics calendars from events.yaml")
    ap.add_argument("--only", nargs="*", help="only these calendar ids")
    ap.add_argument("--check", action="store_true", help="parse only, do not write files")
    args = ap.parse_args()

    if not EVENTS_FILE.exists():
        print(f"ERROR: {EVENTS_FILE} not found. Create it first (Phase 3).", file=sys.stderr)
        return 2

    data = yaml.safe_load(EVENTS_FILE.read_text()) or {}
    calendars = data.get("calendars") or []
    if not calendars:
        print("ERROR: no calendars defined in events.yaml", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(exist_ok=True)
    written, total_events = 0, 0
    for cal in calendars:
        if args.only and cal["id"] not in args.only:
            continue
        n = len(cal.get("events") or [])
        if n == 0:
            # Skip empty calendars (e.g. a category currently covered only by a
            # subscribed feed). Emitting a 0-event .ics is invalid RFC 5545.
            print(f"  skip  {cal['id']}: 0 events (nothing to generate)")
            continue
        cal_id, c = build_calendar(cal)
        total_events += n
        if args.check:
            print(f"  ok  {cal_id}: {n} events (not written)")
            continue
        out = OUT_DIR / f"{cal_id}.ics"
        out.write_bytes(c.to_ical())
        written += 1
        print(f"  wrote {out.relative_to(ROOT)} ({n} events)")

    print(f"\nDone. {written} calendar(s), {total_events} event(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

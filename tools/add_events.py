#!/usr/bin/env python3
"""
add_events.py — Append events into existing calendars in data/events.yaml.

Part of the Pyros World Events Calendar (WAT framework, tools layer).

Unlike merge_parts.py (which REPLACES a calendar's whole event list), this tool
ADDS events to an existing calendar without disturbing what's already there. It
reads data/parts/add-*.yaml files, each shaped:

    target: combat-sports
    events:
      - summary: "..."
        start: "YYYY-MM-DD"
        ...

Events are de-duplicated against the target calendar by (normalised summary,
start), so re-running is safe and won't create duplicates.

Usage:
    python tools/add_events.py            # apply all data/parts/add-*.yaml
    python tools/add_events.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "data" / "events.yaml"
PARTS_DIR = ROOT / "data" / "parts"


def norm(summary: str) -> str:
    # Ignore a leading [TBC] marker and case/space when comparing.
    s = re.sub(r"^\s*\[TBC\]\s*", "", str(summary), flags=re.I)
    return re.sub(r"\s+", " ", s).strip().lower()


def key(ev: dict) -> tuple[str, str]:
    return (norm(ev.get("summary", "")), str(ev.get("start", "")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = yaml.safe_load(EVENTS.read_text()) or {}
    by_id = {c["id"]: c for c in data.get("calendars", [])}

    parts = sorted(PARTS_DIR.glob("add-*.yaml"))
    if not parts:
        print("No data/parts/add-*.yaml files found.", file=sys.stderr)
        return 1

    total_added = 0
    for p in parts:
        block = yaml.safe_load(p.read_text()) or {}
        target = block.get("target")
        new_events = block.get("events") or []
        if target not in by_id:
            print(f"  SKIP {p.name}: target '{target}' not found in events.yaml", file=sys.stderr)
            continue
        cal = by_id[target]
        cal.setdefault("events", [])
        existing = {key(e) for e in cal["events"]}
        added = 0
        for ev in new_events:
            if key(ev) in existing:
                continue
            cal["events"].append(ev)
            existing.add(key(ev))
            added += 1
        total_added += added
        print(f"  {p.name} -> {target}: +{added} new "
              f"({len(new_events) - added} already present)")

    if args.dry_run:
        print(f"\n[dry-run] would add {total_added} event(s); not written.")
        return 0

    with EVENTS.open("w") as f:
        f.write("# Pyros World Events Calendar — curated events (single source of truth).\n")
        f.write("# Regenerate calendars after editing: python tools/generate_ics.py\n\n")
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=100)
    print(f"\nAdded {total_added} event(s) into {EVENTS.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

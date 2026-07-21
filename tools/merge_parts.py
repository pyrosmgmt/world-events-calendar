#!/usr/bin/env python3
"""
merge_parts.py — Merge verified per-category blocks into data/events.yaml.

Part of the Pyros World Events Calendar (WAT framework, tools layer).

During a verification pass, each category's confirmed events are written to
data/parts/<id>.yaml (a dict: {id, name, description, events:[...]}). This tool
folds those blocks back into the single source of truth data/events.yaml,
replacing any existing calendar with the same id and appending new ones. The
original calendar ORDER in events.yaml is preserved; new ids are appended.

Usage:
    python tools/merge_parts.py            # merge all data/parts/*.yaml
    python tools/merge_parts.py --dry-run  # show what would change, don't write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "data" / "events.yaml"
PARTS_DIR = ROOT / "data" / "parts"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = yaml.safe_load(EVENTS.read_text()) or {}
    calendars = data.get("calendars") or []
    by_id = {c["id"]: c for c in calendars}
    order = [c["id"] for c in calendars]

    parts = sorted(PARTS_DIR.glob("*.yaml"))
    if not parts:
        print("No part files found in data/parts/", file=sys.stderr)
        return 1

    changed = []
    for p in parts:
        block = yaml.safe_load(p.read_text())
        if not block or "id" not in block:
            print(f"  skip {p.name}: no 'id'", file=sys.stderr)
            continue
        cid = block["id"]
        n = len(block.get("events") or [])
        if cid in by_id:
            old_n = len(by_id[cid].get("events") or [])
            changed.append(f"  update {cid}: {old_n} -> {n} events")
        else:
            order.append(cid)
            changed.append(f"  add    {cid}: {n} events")
        by_id[cid] = block

    print("\n".join(changed) if changed else "  (no changes)")

    if args.dry_run:
        print("\n[dry-run] not written.")
        return 0

    data["calendars"] = [by_id[cid] for cid in order]
    with EVENTS.open("w") as f:
        f.write("# Pyros World Events Calendar — curated events (single source of truth).\n")
        f.write("# Regenerate calendars after editing: python tools/generate_ics.py\n\n")
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)
    print(f"\nMerged {len(parts)} part(s) into {EVENTS.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

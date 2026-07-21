#!/usr/bin/env python3
"""
check_liveness.py — Verify subscribed calendar feeds are live and valid.

Part of the Pyros World Events Calendar (WAT framework, tools layer).

Reads data/feeds_registry.yaml and, for every feed that has a `url`, performs a
real HTTP GET and checks:
  - HTTP 200
  - body contains BEGIN:VCALENDAR
  - parses as a VCALENDAR and reports the VEVENT count
  - reports how many events fall in the future (staleness signal)

Writes a human-readable report to reports/liveness.md and prints a summary.
This is the tool that backs the "no fabricated / dead URLs" success criterion,
and is intended to be re-run during the yearly refresh.

Usage:
    python tools/check_liveness.py
    python tools/check_liveness.py --timeout 30
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

import requests
import yaml
from icalendar import Calendar

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "feeds_registry.yaml"
REPORT = ROOT / "reports" / "liveness.md"

UA = "Mozilla/5.0 (compatible; PyrosCalendarBot/1.0; +content-planning)"


def check_url(url: str, timeout: int) -> dict:
    result = {"url": url, "ok": False, "status": None, "events": None,
              "future": None, "note": ""}
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": UA},
                            allow_redirects=True)
        result["status"] = resp.status_code
        if resp.status_code != 200:
            result["note"] = f"HTTP {resp.status_code}"
            return result
        body = resp.content
        if b"BEGIN:VCALENDAR" not in body:
            result["note"] = "response is not an iCalendar (no BEGIN:VCALENDAR)"
            return result
        cal = Calendar.from_ical(body)
        events = [c for c in cal.walk("VEVENT")]
        today = date.today()
        future = 0
        for ev in events:
            dt = ev.get("dtstart")
            if dt is None:
                continue
            v = dt.dt
            d = v.date() if isinstance(v, datetime) else v
            if isinstance(d, date) and d >= today:
                future += 1
        result.update(ok=True, events=len(events), future=future)
        if len(events) == 0:
            result["note"] = "valid calendar but 0 events"
        elif future == 0:
            result["note"] = "no future events (possibly stale)"
        return result
    except requests.RequestException as exc:
        result["note"] = f"request error: {exc}"
        return result
    except Exception as exc:  # noqa: BLE001 — parse errors etc.
        result["note"] = f"parse error: {exc}"
        return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Check subscribed feed liveness")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    if not REGISTRY.exists():
        print(f"ERROR: {REGISTRY} not found. Build it from research first (Phase 2).",
              file=sys.stderr)
        return 2

    data = yaml.safe_load(REGISTRY.read_text()) or {}
    # Only check actual iCalendar feeds. 'reference' entries (e.g. gov.uk JSON) are
    # cross-check data sources, not .ics feeds, so they're excluded.
    feeds = [f for f in (data.get("feeds") or [])
             if f.get("url") and f.get("strategy") != "reference"]
    if not feeds:
        print("No feeds with URLs to check.", file=sys.stderr)
        return 0

    lines = ["# Feed Liveness Report", ""]
    lines.append(f"Checked {len(feeds)} feed(s).")
    lines.append("")
    lines.append("| Category | Provider | Status | Events | Future | Note |")
    lines.append("|---|---|---|---|---|---|")

    ok_count = 0
    for f in feeds:
        r = check_url(f["url"], args.timeout)
        mark = "✅" if r["ok"] and not r["note"] else ("⚠️" if r["ok"] else "❌")
        if r["ok"]:
            ok_count += 1
        lines.append(
            f"| {f.get('category','')} | {f.get('provider','')} | {mark} "
            f"{r['status'] or ''} | {r['events'] if r['events'] is not None else '-'} "
            f"| {r['future'] if r['future'] is not None else '-'} | {r['note']} |"
        )
        print(f"{mark} {f.get('provider','?')}: {r['status']} "
              f"events={r['events']} future={r['future']} {r['note']}")

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"\n{ok_count}/{len(feeds)} feed(s) reachable & valid. Report: {REPORT.relative_to(ROOT)}")
    return 0 if ok_count == len(feeds) else 1


if __name__ == "__main__":
    raise SystemExit(main())

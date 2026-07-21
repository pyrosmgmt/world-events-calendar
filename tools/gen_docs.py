#!/usr/bin/env python3
"""
gen_docs.py — Generate reports from the registry + events (so docs never drift).

Part of the Pyros World Events Calendar (WAT framework, tools layer).

Reads data/feeds_registry.yaml and data/events.yaml and writes:
  - reports/provider_comparison.md — every researched feed, strategy, price, cadence
  - reports/coverage.md            — per-category coverage: strategy + event counts

Usage:
    python tools/gen_docs.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "feeds_registry.yaml"
EVENTS = ROOT / "data" / "events.yaml"
REPORTS = ROOT / "reports"

CATEGORY_ORDER = [
    "uk-sporting", "us-sporting", "global-sporting", "combat-sports", "motorsport",
    "gaming", "entertainment-pop-culture", "music-festivals", "shopping-events",
    "holidays-awareness", "technology-social-media", "space-science",
]


def load():
    reg = yaml.safe_load(REGISTRY.read_text()) or {}
    ev = yaml.safe_load(EVENTS.read_text()) or {}
    return reg, ev


def provider_comparison(reg) -> str:
    feeds = reg.get("feeds") or []
    lines = ["# Provider Comparison", ""]
    lines.append(f"Verified on {reg.get('meta', {}).get('verified_on', 'n/a')}. "
                 "Feeds with a URL were fetched live and parsed as valid iCalendar.")
    lines.append("")
    lines.append("| Category | Provider | Strategy | Official | Price | Cadence | Confidence | Live URL |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for f in feeds:
        url = "yes" if f.get("url") else "—"
        lines.append(
            f"| {f.get('category','')} | {f.get('provider','')} | {f.get('strategy','')} "
            f"| {'yes' if f.get('official') else 'no'} | {f.get('price','')} "
            f"| {f.get('cadence','')} | {f.get('confidence','')} | {url} |"
        )
    return "\n".join(lines) + "\n"


def coverage(reg, ev) -> str:
    feeds = reg.get("feeds") or []
    strat_by_cat: dict[str, list[str]] = {}
    for f in feeds:
        strat_by_cat.setdefault(f["category"], []).append(f.get("strategy", "?"))

    counts: dict[str, dict] = {}
    for cal in ev.get("calendars") or []:
        evs = cal.get("events") or []
        tbc = sum(1 for e in evs if str(e.get("summary", "")).startswith("[TBC]")
                  or str(e.get("notes", "")).upper().startswith("TENTATIVE"))
        counts[cal["id"]] = {"total": len(evs), "tbc": tbc}

    lines = ["# Coverage Report", ""]
    lines.append("Per-category coverage. **Subscribe** = zero-maintenance official/third-party "
                 "feed. **Custom** = generated from events.yaml (yearly refresh). "
                 "**Hybrid** = subscribe feed + curated top-up.")
    lines.append("")
    lines.append("| Category | Strategy | Curated events | Firm | [TBC] |")
    lines.append("|---|---|---|---|---|")
    total = firm = tbc_total = 0
    for cat in CATEGORY_ORDER:
        strat = "/".join(sorted(set(strat_by_cat.get(cat, ["—"]))))
        c = counts.get(cat, {"total": 0, "tbc": 0})
        firm_n = c["total"] - c["tbc"]
        total += c["total"]; firm += firm_n; tbc_total += c["tbc"]
        lines.append(f"| {cat} | {strat} | {c['total']} | {firm_n} | {c['tbc']} |")
    lines.append(f"| **TOTAL** | | **{total}** | **{firm}** | **{tbc_total}** |")
    lines.append("")
    lines.append("> Curated-event counts exclude events delivered purely by a subscribed feed "
                 "(e.g. UFC, F1, public holidays), which are unbounded and auto-updating.")
    return "\n".join(lines) + "\n"


def main() -> int:
    reg, ev = load()
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "provider_comparison.md").write_text(provider_comparison(reg))
    (REPORTS / "coverage.md").write_text(coverage(reg, ev))
    print("Wrote reports/provider_comparison.md and reports/coverage.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

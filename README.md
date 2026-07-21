# Pyros World Events Calendar

A content-planning **tentpole calendar** for the Pyros team: the big cultural,
sporting, and entertainment moments coming up, split into 12 category calendars so
the team can plan promotions around them. Events are **broad tentpole moments**
(e.g. "FIFA World Cup", not each match).

See [`SPEC.md`](SPEC.md) for the full agreed specification.

## The stack

Only 4 categories have true zero-maintenance auto-updating feeds; the rest are
small, accuracy-checked custom calendars refreshed once a year. Full detail in
[`reports/provider_comparison.md`](reports/provider_comparison.md) and
[`reports/coverage.md`](reports/coverage.md).

| Category | Strategy | Source |
|---|---|---|
| Holidays & Awareness | ✅ Subscribe + curated awareness days | Google official UK/US holiday feeds |
| Combat Sports | ✅ Subscribe (UFC) + curated boxing | clarencechaan UFC feed |
| Motorsport | ✅ Subscribe (F1) + curated non-F1 | f1calendar.com feed |
| Technology | 🔶 Hybrid | Techmeme feed + curated keynotes |
| Space & Science | 🔶 Hybrid | in-the-sky.org + curated launches |
| Entertainment | 🔶 Hybrid | AddEvent awards feed + curated films |
| Shopping | ⚙️ Custom (rule-based) | Deterministic date rules |
| UK / US / Global Sport | ⚙️ Custom | ESPN API + governing bodies |
| Gaming | ⚙️ Custom | IGDB + official showcases |
| Music & Festivals | ⚙️ Custom | Official festival sites |

Every recommended feed URL was fetched live and confirmed as a valid iCalendar
during research (2026-07-21). Rejected/unverified candidates — including several
"AI-curated" feeds that contained hallucinated or duplicated events — are
documented per category in [`research/`](research/).

## Quick start

```bash
# one-time setup
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt

# generate calendars from the curated source of truth
./.venv/bin/python tools/generate_ics.py
./.venv/bin/python tools/validate_ics.py      # must report 0 errors

# check the subscribed feeds are alive
./.venv/bin/python tools/check_liveness.py

# regenerate the reports
./.venv/bin/python tools/gen_docs.py
```

To add the calendars to Google Calendar, see
[`guides/subscription_guide.md`](guides/subscription_guide.md).

## How it's organised (WAT framework)

```
data/
  events.yaml          # SINGLE SOURCE OF TRUTH — curated tentpole events (edit this)
  feeds_registry.yaml  # researched providers: url, strategy, price, cadence, confidence
  parts/               # per-category verified blocks, merged into events.yaml
tools/
  generate_ics.py      # events.yaml -> calendars/*.ics  (UTC + VTIMEZONE, stable UIDs)
  validate_ics.py      # RFC-5545 checks; fails on errors
  check_liveness.py    # HTTP + valid-VCALENDAR check for subscribed feeds
  merge_parts.py       # fold data/parts/*.yaml into events.yaml
  gen_docs.py          # build reports/ from the registry (docs never drift)
workflows/             # SOPs: research, generate, yearly refresh, publish to Google
calendars/             # generated .ics files (the deliverables)
research/              # per-category research evidence (verified + rejected feeds)
guides/                # subscription guide, maintenance guide
reports/               # coverage, provider comparison, liveness, verification log
```

## Maintenance

~1–2 hours once a year (the auto-feeds need nothing). See
[`guides/maintenance_guide.md`](guides/maintenance_guide.md) and
[`workflows/yearly_refresh.md`](workflows/yearly_refresh.md).

## Data integrity

- No fabricated URLs or providers — every feed was fetched and parsed live.
- Every curated event carries a **source link** and a **verified date**.
- Events with an unconfirmed date are prefixed **[TBC]** and flagged in notes.

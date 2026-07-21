# Pyros World Events Calendar — Specification (v2, agreed)

## Purpose
A **content-planning tentpole calendar** for the Pyros team. It surfaces the big
cultural, sporting, and entertainment moments coming up so models and the team
can plan promotions and content around them.

Events are **broad tentpole moments**, not individual fixtures. Example: one entry
for "FIFA World Cup 2026" spanning the whole tournament — **not** 64 match entries.

## Consumers
The Pyros team, planning promotions. Each person subscribes to the category
calendars relevant to them.

## Delivery
- One `.ics` per category.
- **Primary:** official, auto-updating public feeds where they exist (zero maintenance).
- **Fallback:** custom `.ics` we generate from a reviewable source file, hosted at a
  stable HTTPS URL (GitHub Pages by default; host-swappable) so subscriptions stay live.
- Raw `.ics` also produced for one-time import.
- **Final step:** load all calendars into the Pyros Google Calendar account via the
  connected Google Calendar tool.

## Priority (explicit)
Feeds must be **correct** and require **little to no maintenance**. Preference order
for every category:
1. Official auto-updating public feed (zero maintenance) — best.
2. Public API → generated feed (yearly refresh).
3. Curated + verified list (yearly refresh) — only where nothing better exists.

## Categories (12)
Each event lives in **exactly one primary category** (no duplicates across calendars).

1. UK Sporting Events
2. US Sporting Events
3. Global Sporting Events
4. Combat Sports
5. Motorsport
6. Gaming
7. Entertainment & Pop Culture
8. Music & Festivals
9. Shopping Events
10. Holidays & Awareness
11. Technology & Social Media
12. Space & Science

## Scope
- Broad tentpole events only.
- Time window: **2026-07-21 → 2027-12-31** (extended to end of 2027; refresh here for the
  2028 calendar). Events 12–18 months out that aren't officially dated yet are included
  as best-estimates prefixed `[TBC]`.
- Refreshed yearly.

## Data integrity rules
- **No fabricated URLs or providers.** Every feed/event carries `source_url` and
  `last_verified` (date).
- A feed is only "verified" if it was fetched live and parsed as a valid `VCALENDAR`.
- Times stored in UTC with proper `VTIMEZONE`.

## Architecture (WAT framework)
```
data/
  events.yaml          # single source of truth for custom/tentpole events (human-reviewable)
  feeds_registry.yaml  # researched providers: url, official?, price, cadence, confidence, legal, last_verified
tools/
  generate_ics.py      # events.yaml -> calendars/*.ics (icalendar lib, UTC + VTIMEZONE)
  validate_ics.py      # validates generated + subscribed feeds
  check_liveness.py    # HTTP 200 + valid VCALENDAR + sane event count/date range
workflows/
  research_feeds.md    # SOP: how per-category research + verification is done
  generate_calendars.md
  yearly_refresh.md    # SOP: the once-a-year maintenance run
  publish_to_google.md # SOP: load calendars into Pyros Google Calendar
calendars/             # generated .ics files
research/              # per-category research notes (evidence)
guides/                # subscription/install guide, maintenance guide
reports/               # coverage report, provider comparison (generated from registry)
```

## Success criteria (measurable)
- Every category has either ≥1 verified official/public feed **or** a documented
  "custom-built" decision with a named data source.
- Every event has `source_url` + `last_verified`.
- `validate_ics.py` passes: valid VCALENDAR, UTC, not past-only.
- `check_liveness.py` green for all subscribed feeds.
- All calendars loaded into the Pyros Google Calendar.

## Build phases
1. Scaffold + SPEC.md  ✅
2. Per-category research → `feeds_registry.yaml`
3. Curate `events.yaml`  ← **review checkpoint**
4. Build tools
5. Generate + validate
6. Docs (generated from registry)
7. Host feeds + load into Pyros Google Calendar

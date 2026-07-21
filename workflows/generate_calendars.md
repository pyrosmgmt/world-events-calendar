# Workflow: Generate & Validate Calendars

**Objective:** Turn the reviewed `data/events.yaml` into validated `.ics` files in
`calendars/`.

## Inputs
- `data/events.yaml` — the single source of truth for custom/curated calendars.
- Python venv with `icalendar`, `pyyaml` (`requirements.txt`).

## Steps
1. Activate env: `./.venv/bin/python` (or `pip install -r requirements.txt`).
2. Parse-check first (no writes):
   `./.venv/bin/python tools/generate_ics.py --check`
3. Generate all: `./.venv/bin/python tools/generate_ics.py`
   - Or a subset: `... --only shopping-events holidays-awareness`
4. Validate: `./.venv/bin/python tools/validate_ics.py`
   - Must report **0 errors**. WARN (e.g. "all events in the past") is acceptable
     only if intentional; usually it means the calendar needs a refresh.
5. Commit the regenerated `.ics` files.

## Event schema (events.yaml)
```yaml
calendars:
  - id: shopping-events            # becomes calendars/shopping-events.ics
    name: "Pyros · Shopping Events"
    description: "..."
    events:
      - summary: "Black Friday"
        start: "2026-11-27"        # DATE => all-day; DATETIME (with T) => timed
        end:   "2026-11-27"        # optional; INCLUSIVE last day for all-day
        tz:    "Europe/London"     # required only for timed events
        source_url: "https://..."  # provenance (required for integrity)
        last_verified: "2026-07-21"
        notes: "free text; shown in the event description"
```

## Rules / gotchas
- All-day `end` is the **inclusive** last day; the generator converts to the
  RFC-5545 exclusive DTEND automatically. Single-day events omit `end`.
- Timed events **must** set `tz` (IANA name). The generator emits the VTIMEZONE.
- UIDs are derived from `summary` + start date and are **stable** — editing a
  date creates a new UID (old event lingers on subscribers until removed). For a
  moved event, keep an explicit `uid:` field so it updates in place.
- Each event should have `source_url` + `last_verified`; the validator/reports
  rely on it and it satisfies the "no fabricated data" success criterion.

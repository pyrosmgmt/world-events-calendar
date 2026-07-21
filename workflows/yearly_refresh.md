# Workflow: Yearly Refresh (Maintenance SOP)

**Objective:** Once a year (recommended: **early December**, when next-year tentpole
dates are mostly published), refresh the custom calendars and re-verify the
subscribed feeds. Target effort: ~1–2 hours total.

> The subscribed official feeds (Google holidays, UFC) are **auto-updating and need
> no work** — this SOP only covers the custom/curated calendars and a health check.

## 1. Health-check the subscribed feeds (5 min)
```
./.venv/bin/python tools/check_liveness.py
```
- Open `reports/liveness.md`. Every subscribed feed should be ✅.
- If one is ❌ (dead) or ⚠️ (0 future events / stale), find a replacement (see
  `research/<category>.md` for alternates) and update `data/feeds_registry.yaml`.

## 2. Refresh custom calendars (bulk of the work)
For each custom calendar, update `data/events.yaml`:
- **Deterministic-date events** (most Shopping, some Holidays): the dates follow a
  rule (e.g. Black Friday = 4th Thursday of Nov + 1). Recompute for the new window.
- **Fixed annual events** (CES, MWC, festivals): confirm next year's dates from the
  official site listed in `source_url`; update `start`/`end` + bump `last_verified`.
- **Volatile events** (game launches, boxing cards, rocket launches): re-pull from
  the named source, keep only what's confirmed, mark tentative ones in `notes`.
- Add newly announced tentpoles; drop events that have passed out of the window.

Per-category source of truth is in each `research/<category>.md` "Recommendation".

## 3. Regenerate & validate
```
./.venv/bin/python tools/generate_ics.py
./.venv/bin/python tools/validate_ics.py     # must be 0 errors
```

## 4. Publish
- Push regenerated `.ics` to the host (GitHub Pages) — subscribers auto-update.
- If maintaining the Google Calendar copies, re-run `workflows/publish_to_google.md`.

## 5. Record
- Append a dated line to `reports/verification_log.md` noting what changed and the
  date verified. This is the audit trail behind the "no fabricated/stale data" rule.

## Known volatility flags (watch these)
| Category | Risk | Mitigation |
|---|---|---|
| Gaming launches | Dates slip often | Re-pull quarterly; mark tentative |
| Boxing / crossover | Cards announced late | Light quarterly curate |
| Space launches | Constant slips | Prefer eclipses/meteor showers (fixed); mark launches tentative |
| Amazon Prime Day | No fixed rule, moves | Confirm yearly from Amazon Newsroom |
| Playoff finals (US/global) | Exact date locks mid-season | Use league window, tighten when known |

# Maintenance Guide

**How much work is this?** Roughly **1–2 hours, once a year**. The 4 auto-updating
feeds (UK/US holidays, UFC, F1) need **zero** work. Only the curated calendars need
a refresh, and most of their dates follow fixed rules or are announced a year ahead.

## When
Do the refresh in **early December**, when most of the next year's tentpole dates
have been published. Add a recurring reminder.

## What to do
Follow the step-by-step SOP in [`workflows/yearly_refresh.md`](../workflows/yearly_refresh.md).
In short:

1. **Check the feeds are alive:** `python tools/check_liveness.py` → review
   `reports/liveness.md`. Replace any dead feed (alternatives are in `research/`).
2. **Update `data/events.yaml`** with next year's dates:
   - Shopping/holidays: mostly rule-based — recompute.
   - Fixed annual events (CES, festivals, awards): confirm on the official site in
     each event's `source_url`.
   - Volatile (game launches, boxing, launches): re-pull, keep only confirmed,
     mark the rest `[TBC]`.
3. **Regenerate & validate:**
   `python tools/generate_ics.py && python tools/validate_ics.py` (must be 0 errors).
4. **Republish** the `.ics` files (see `workflows/publish_to_google.md`).
5. **Log it** in `reports/verification_log.md`.

## The `[TBC]` convention
Events whose date isn't officially confirmed have `[TBC]` in the title and a
`TENTATIVE:` note. During the refresh, try to confirm them and drop the `[TBC]`
prefix once you have an official date.

## Volatility cheat-sheet
| Watch | Why | Do |
|---|---|---|
| Amazon Prime Day | No fixed rule | Confirm from Amazon Newsroom each year |
| Game launches | Slip often | Re-pull quarterly; keep `[TBC]` until gold |
| Boxing cards | Announced ~2–3 mo ahead | Light quarterly top-up |
| Playoff finals | Exact date locks mid-season | Widen then tighten |
| Rocket launches | Constant slips | Prefer eclipses/showers; mark launches `[TBC]` |

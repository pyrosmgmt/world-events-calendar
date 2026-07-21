# Workflow: Research & Verify Feeds

**Objective:** For a category, find the best calendar source and record it in
`data/feeds_registry.yaml`, with evidence in `research/<category>.md`.

## Priority order (always)
1. Official auto-updating public `.ics` feed (zero maintenance) — best.
2. Public API we can build a feed from (yearly refresh).
3. Curated + verified list (yearly refresh) — only if nothing better exists.

## Steps
1. Search for candidate feeds/APIs (official governing bodies first, then
   reputable third parties).
2. **Verify liveness** — actually fetch each candidate URL and confirm the body
   contains `BEGIN:VCALENDAR` with real `VEVENT`s. Record HTTP status + a snippet.
   A feed you couldn't fetch is **UNVERIFIED** and must not be recommended.
3. **Check granularity** — we want broad tentpole events, not per-fixture noise.
   Reject feeds that only offer every-single-game granularity.
4. **Check accuracy** — spot-check dates against an official source. Reject feeds
   with hallucinated, duplicated, or wrongly-cancelled events (several
   "AI-curated" feeds fail here).
5. Record in `feeds_registry.yaml`: provider, url, strategy (subscribe/custom/
   hybrid), official?, price, cadence, confidence, legal note, `last_verified`.
6. Write full findings (verified + rejected) to `research/<category>.md`.

## Rules
- **Never invent or guess a URL.** Only record URLs actually retrieved.
- Prefer official over third-party even if the third party is more convenient.
- Note any ToS/legal concern (e.g. IGDB is non-commercial-only).
- Re-run `tools/check_liveness.py` after updating the registry.

# Verification Log

Audit trail for the "no fabricated / stale data" success criterion. Append a dated
entry whenever feeds or events are verified or refreshed.

---

## 2026-07-21 — Initial build

**Feed research (12 categories).** Each category researched by a dedicated pass;
every recommended feed URL fetched live and confirmed as a valid `VCALENDAR`.
Results in `data/feeds_registry.yaml`; evidence + rejected candidates in `research/`.

Zero-maintenance auto-updating feeds verified live:
- Google UK holidays, Google US holidays (official)
- UFC — clarencechaan/ufc-cal (per-card)
- F1 — f1calendar.com (per Grand Prix)

Notable rejections (accuracy): Smart Calendars AI festival feeds (hallucinated
events, false `[CANCELLED]` tags, 3× duplicates); several dead/empty feeds
(CalendarLabs FIFA 0 bytes, XerBlade movies last event 2022).

**Event curation.** `data/events.yaml` compiled from research — broad tentpole
events only, window 2026-07-21 → 2027-07-31, every event carrying `source_url` +
`last_verified`.

**Date verification pass.** Tentative dates confirmed against official sources
where possible; unconfirmable dates prefixed `[TBC]`. Per-category outcomes:
- gaming — corrected TGS (Sep 17–21), CoD MW4 (Oct 23), LoL Worlds final (Nov 14);
  added GTA VI (Nov 19 2026, official). EA FC 27 + Summer Game Fest 2027 left `[TBC]`.
- us-sporting — corrected Super Bowl LXI (Feb 14, was Feb 7), CFP Championship
  (Jan 25, was Jan 11), NFL playoffs start (Jan 16). Added MLB Opening Day, US Open
  (golf). NHL/NBA Finals G1 left `[TBC]` (playoff-dependent).
- uk-sporting — removed a PHANTOM Ashes fixture (2025-26 away series already
  concluded); corrected Boat Race (Apr 11) and London Marathon (Apr 24–25). Home
  Ashes 2027 Test dates left `[TBC]` (ECB not yet published).
- global-sporting — corrected UCL Final (Jun 5 2027), Rugby Nations Championship
  final (Nov 29). Added Tour de France 2027 (Edinburgh Grand Départ).
- motorsport — all 7 non-F1 confirmed; Daytona 500 moved to Feb 21 (Super Bowl
  clash), Rolex 24 to Jan 30–31, Petit Le Mans Oct 3, Valencia MotoGP Nov 22.
- entertainment — corrected VMAs (Sep 27, was Sep 6), Grammys (Feb 7), Critics
  Choice (Jan 3), SAG (Feb 28), BET (Jun 28). Added 3 confirmed blockbusters
  (Spider-Man, Avengers: Doomsday, Star Wars: Starfighter). Tony Awards `[TBC]`.
- technology — confirmed CES 2027 (Jan 6–9), MWC (Mar 1–4), Computex, Ignite,
  Meta Connect, Snapdragon Summit. Apple/Google 2027 keynotes left `[TBC]`.
- music-festivals — confirmed Coachella, Glastonbury (2027 after 2026 fallow),
  EDC LV, Ultra from official sites. Tomorrowland Belgium 2027 `[TBC]`.
- combat-sports — curated 18 marquee boxing + Misfits crossover cards from
  CBS/Sky/DAZN schedules (UFC stays on its own auto feed).

**Result:** 137 curated events — **124 firm**, 13 `[TBC]` (genuinely undetermined).
All 7 subscribed feeds verified live (`reports/liveness.md`). All 12 `.ics` files
pass `validate_ics.py` with 0 errors.

Residual caveats: BAFTA + BET (entertainment) rest on official-headline search
results (official pages geo-blocked at fetch time); some near-term boxing cards are
schedule-sourced (CBS/Sky) rather than promoter-confirmed. Re-verify at refresh.

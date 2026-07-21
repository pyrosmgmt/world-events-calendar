# Gaming — Tentpole Calendar Feed Research

**Category:** Gaming (major game launches + industry moments)
**Prepared for:** Pyros content-planning "tentpole" calendar
**Date:** 2026-07-21
**Target window:** rolling ~12 months (2026-07 → 2027-07)
**Granularity wanted:** BROAD tentpoles only — big AAA launches (GTA VI, CoD annual, EA Sports FC, etc.), industry showcases (Summer Game Fest, Gamescom, Tokyo Game Show, The Game Awards), major esports finals (LoL Worlds). One entry per notable release/event — NOT every indie title.

---

## TL;DR

No single official, auto-updating .ics feed exists that matches the curated "tentpole" granularity. The two live feeds I verified are each wrong in opposite directions: OpenCritic lists *every* game release (thousands, mostly historical), and Events for Gamers lists *B2B dev conferences* (mostly minor, and missing launches + the biggest showcases). **Recommendation: build a custom curated, yearly-refreshed calendar** seeded from IGDB (release dates + popularity) for launches and from official showcase announcements/Wikipedia for events. Details and reasoning below.

---

## Verified options (fetched live, confirmed real iCalendar)

### 1. OpenCritic — official game-release calendar
- **Feed URL:** `https://img.opencritic.com/calendar/OpenCritic.ics`
- **Official?** Yes (OpenCritic's own published calendar, linked from https://opencritic.com/calendar)
- **Price:** Free
- **Verification:** HTTP 200, `Content-Type: text/calendar`, ~2.26 MB. Contains `BEGIN:VCALENDAR` and **6,527 `VEVENT`s**. Evidence snippet:
  ```
  BEGIN:VEVENT
  DTSTART;VALUE=DATE:20260424
  SUMMARY:Pragmata (PS5 version)  ... (from the r-salas feed)
  ```
  OpenCritic evidence: summaries such as `Final Fantasy X / X-2 HD Remaster Release`, `Wolfenstein: The Old Blood Release`, `Tropico 5 Release`.
- **Update cadence:** Auto-updating (OpenCritic regenerates it).
- **Maintenance burden:** Zero (if used as-is).
- **Reliability:** High (established site, CDN-hosted `img.opencritic.com`).
- **Granularity fit:** ❌ **Too granular AND skewed historical.** It is one event per *game release* (even split per-platform in some cases), dominated by past releases. Of 6,526 dated events, the date range runs 1970→2027-02 and **only ~12 events are dated on/after today (2026-07-21)** — most upcoming AAA titles with unconfirmed dates are not present. Unusable directly for a clean tentpole view; would require heavy filtering every refresh.
- **ToS:** No explicit public-feed license found; it is a publicly published subscribe link. Re-publishing wholesale to clients could raise attribution questions — flag if redistributed.

### 2. Events for Gamers — industry events / conferences calendar
- **Feed URL (webcal):** `webcal://www.eventsforgamers.com/?post_type=tribe_events&ical=1&eventDisplay=list`
- **Feed URL (https, what actually fetches):** `https://www.eventsforgamers.com/?post_type=tribe_events&ical=1&eventDisplay=list`
- **Official?** No (third-party aggregator; WordPress "The Events Calendar" / `tribe_events` plugin export).
- **Price:** Free
- **Verification:** HTTP 200, `Content-Type: text/calendar; charset=UTF-8`. Contains `BEGIN:VCALENDAR`; ~30 `VEVENT`s in the default window, ~70 dated events spanning 2025→2027, ~47 future. Evidence: `SIGGRAPH 2026`, `Gen Con 2026`, `QuakeCon 2026`, `gamescom 2026`, `ChinaJoy 2026`.
- **Update cadence:** Rolling as the site adds events (list view is a moving window; paginate with `&tribe-bar-date=YYYY-MM-DD`).
- **Maintenance burden:** Low if used as-is, but see fit.
- **Reliability:** Medium (small third-party site; feed shape depends on their WP plugin staying up).
- **Granularity fit:** ❌ **Wrong content for tentpoles.** Heavily weighted to minor/local dev conferences and expos (e.g. `MeetToMatch`, `Philippine GameDev Expo`, `Nottingham Video Games Expo`, `2D Con`, `Save the Games Symposium`). It DOES include a few real tentpoles (gamescom, ChinaJoy, QuakeCon, Gen Con) but **MISSES Summer Game Fest, The Game Awards, Tokyo Game Show, GDC, PAX, and all game launches and esports finals** in the checked window. Too noisy and too incomplete.

### 3. r-salas/ical-videogames — self-hostable game-release feed (context)
- **Cloud feed URL (example):** `https://ical-videogames.onrender.com/calendar?platform=ps5&region=pal`
- **Source repo:** https://github.com/r-salas/ical-videogames
- **Official?** No (personal open-source project).
- **Price:** Free.
- **Verification:** HTTP 200, valid `BEGIN:VCALENDAR`, 19 `VEVENT`s for PS5/PAL. Snippet: `SUMMARY:Pragmata (PS5 version)`, `SUMMARY:Lego Batman: Legacy of the Dark Knight (PS5 version)`.
- **Data source:** Scrapes Wikipedia "List of \<platform\> games" pages; data cached in .pkl files, refreshed by a populate task.
- **Granularity fit:** ❌ Too granular (every game, split per platform). Also runs on a **free Render instance** (cold-starts / can disappear) → not maintenance-free or reliable for a client deliverable. Listed only to document that it was checked.

---

## Rejected / unverified options

- **Smart Calendars AI — `game-awards-summer-game-fest` feed** (`https://www.smartcalendars.ai/en/feeds/game-awards-summer-game-fest`): claims a free subscribable .ics for the SGF/TGA showcase cycle. **UNVERIFIED** — the page blocked automated fetches (returned no body / error) so I could not retrieve a working `.ics` URL or confirm `VCALENDAR`. Per verification rules, NOT recommended until a live feed URL can be confirmed in a browser. Worth a manual look if a showcase-only feed is desired.
- **TechRaptor Game Release Calendar** (`techraptor.net`): advertises an .ics download of current calendar contents. **UNVERIFIED** — page blocked automated fetch; no confirmable `.ics` URL retrieved. Also per-game granularity, so likely too granular even if verified.
- **Webnetic / game-releases.com / OpenCritic-style per-game calendars:** all per-title release trackers → too granular for tentpole; not verified.
- **GamesRecap, GameConfGuide, TimesOfGames, GameSpot showcase pages:** editorial lists, not iCalendar feeds. Useful as human data sources, not as subscribe feeds.

---

## API option (for a built feed)

### IGDB API (Internet Game Database, owned by Twitch/Amazon)
- **Docs:** https://api-docs.igdb.com/  (endpoints incl. `release_dates`, `games`, `popularity_primitives`)
- **Auth:** Twitch OAuth2 (Client-ID + bearer token from a free Twitch Developer app).
- **Price / ToS:** **Free for non-commercial use** under the Twitch Developer Services Agreement. ⚠️ **ToS flag:** Pyros is a commercial agency; using IGDB to drive a client-facing planning calendar may fall outside "non-commercial." Review the agreement (or keep the derived calendar internal/non-monetised) before relying on it.
- **Why it fits:** `release_dates` gives concrete/patched dates per game per region; `popularity_primitives` / hype and rating fields let us **filter to only high-profile (tentpole) launches**, avoiding the "every indie game" problem. Best structured, authoritative source for launch dates.
- **Maintenance:** Build once; re-run a script on a yearly (or quarterly) refresh. Because game dates slip constantly, a periodic re-pull is exactly the right correction mechanism.

---

## Reliability / accuracy notes

- **Game release dates slip frequently.** Any launch-based calendar will go stale; favour an approach that is trivially re-generated on a schedule (a script pull), and set entries to the *announced* date with a note to re-verify each quarter.
- **Showcase/event dates are more stable** and usually announced 6–12 months out (Gamescom is fixed annually in Cologne in Aug; Tokyo Game Show late Sep; The Game Awards early–mid Dec; Summer Game Fest early–mid Jun). These can be hand-entered with high confidence.
- **Esports finals** (e.g. LoL Worlds) are announced per-season by the organiser (Riot) — pull dates yearly from the official esports site.

---

## FINAL RECOMMENDATION

**Build a custom curated, yearly-refreshed "Gaming Tentpole" calendar** (Preference tier 2/3). No official auto-updating feed matches the required granularity: OpenCritic (verified, official, zero-maintenance) is too granular and mostly historical; Events for Gamers (verified) is minor B2B conferences and misses the big moments.

Recommended construction:

1. **Launches (AAA tentpoles):** seed from **IGDB API** `release_dates` filtered by popularity/hype to only major titles (GTA VI, annual Call of Duty, EA Sports FC, major first-party Nintendo/Sony/Xbox, etc.). Fallback/cross-check source: **Wikipedia "2026 in video games" / "2027 in video games"** and GamesRadar's release-date roundup. Re-pull quarterly because dates slip. *(Mind the IGDB non-commercial ToS flag above.)*
2. **Industry showcases (hand-entered, stable):** Summer Game Fest (early–mid Jun), Gamescom (Cologne, late Aug), Tokyo Game Show (late Sep), PAX West/East, The Game Awards (early–mid Dec). Confirm exact dates yearly from each event's official site.
3. **Esports finals:** League of Legends Worlds (+ optional Valorant Champions, The International) — pull dates yearly from the official esports sites.

If a low-effort partial feed is wanted *today* without building anything: OpenCritic's official `https://img.opencritic.com/calendar/OpenCritic.ics` is the only verified official launch feed, but it must be filtered down to marquee titles before use — not recommended as-is.

**Key tentpole events for this category:** GTA VI launch, annual Call of Duty, EA Sports FC, major first-party Nintendo/PlayStation/Xbox releases, Summer Game Fest, Gamescom, Tokyo Game Show, The Game Awards, PAX, and major esports finals (LoL Worlds).

**Authoritative data sources:** IGDB API (release dates + popularity), Wikipedia "20XX in video games", GamesRadar release calendar, and each event/esports organiser's official site.

---

### Verification log
| Feed | HTTP | text/calendar | VCALENDAR | VEVENTs | Verdict |
|---|---|---|---|---|---|
| OpenCritic.ics | 200 | yes | yes | 6527 (mostly historical) | Verified; too granular |
| Events for Gamers webcal | 200 | yes | yes | ~30–70 | Verified; wrong content |
| r-salas onrender | 200 | yes | yes | 19 (PS5/PAL) | Verified; too granular + unreliable host |
| Smart Calendars AI | — | — | — | — | UNVERIFIED (blocked) |
| TechRaptor | — | — | — | — | UNVERIFIED (blocked) |

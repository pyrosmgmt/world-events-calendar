# Space & Science — Calendar Feed Research

**Category:** Space & Science tentpole events (major rocket launches, eclipses, meteor-shower peaks, notable astronomical events)
**Prepared:** 2026-07-21 · **Target window:** rolling ~12 months (Jul 2026 → Jul 2027)
**Granularity:** BROAD tentpoles only — one entry per notable event.

> **Key principle for this category:** split the problem in two.
> - **Stable / predictable events** (eclipses, meteor-shower peaks, solstices/equinoxes, supermoons) are computable years in advance and are *safe* to put in a low-maintenance feed.
> - **Volatile events** (rocket launches) slip constantly — dates move by days/weeks with little notice. These must NOT be treated as fixed and should be filtered hard to only notable missions, refreshed frequently.

---

## VERIFIED OPTIONS (fetched live and confirmed real iCalendar)

### 1. Canton Becker "Moon/Astro" calendar — astrocal.ics  ✅ RECOMMENDED (stable events, zero-maintenance)
- **Provider:** cantonbecker.com (independent, long-running personal project)
- **Feed URL:** `https://cantonbecker.com/astronomy-calendar/astrocal.ics`
- **Official?** No (not a government/institutional source, but data is standard astronomical almanac data)
- **Price:** Free
- **Update cadence:** Auto-updating subscription — subscribe once, it rolls forward. Currently covers ~2025 through 2027.
- **Maintenance burden:** ZERO (subscribe-and-forget)
- **Verification:** `HTTP 200`, 74.7 KB, `BEGIN:VCALENDAR` present, **191 VEVENTs**. Confirmed events in-window include:
  - `Total Solar Eclipse (Spain and Mallorca)` (12 Aug 2026), `S. EUROPE / N. AFRICA TOTAL SOLAR ECLIPSE`, `Reminder: Aug 2027 TOTAL Solar Eclipse`, `Total Lunar Eclipse`, `Partial Lunar Eclipse`
  - Meteor showers: `Perseids`, `Geminids "King"`, `Lyrids`, `Leonids`, `Orionids`, `Eta Aquarids`, `Delta Aquariid`, `Draconids`, `Ursids`, `Quadrantids`
  - `June/September/December Solstice`, `March/September Equinox`
- **Granularity fit:** GOOD for tentpoles, but **noisy** — it also includes every moon phase (New/Full/Quarter), cross-quarter pagan dates (e.g. "Lughnasadh"), and mercury retrogrades. For a clean tentpole calendar you would filter to eclipses + meteor peaks + solstices/equinoxes (+ optionally supermoons/full moons).
- **Legal/ToS:** Free for personal/public use; author asks only for a courtesy credit. No commercial licensing barrier for internal planning use.
- **Reliability risk:** Single-maintainer hobby project — small risk it could go stale or offline someday. Mitigate by also keeping the authoritative source (#2) on file.

### 2. In-The-Sky.org — Calendar of Astronomical Events iCal  ✅ RECOMMENDED (authoritative data source for a curated feed)
- **Provider:** in-the-sky.org (Dominic Ford — widely cited, high-quality astronomy reference)
- **Feed URL (per year):** `https://in-the-sky.org/newscalyear_ical.php?year=2026&maxdiff=7` (swap `year=2027`, etc.)
- **Official?** No (independent) but authoritative and precise; effectively the gold-standard free astronomy events source.
- **Price:** Free
- **Update cadence:** Per-year URL. A subscribed calendar re-fetches and stays current within the year; rolling into the next year is a **yearly one-line change** (bump the `year=` param).
- **Maintenance burden:** LOW (annual param bump; or regenerate a curated feed yearly)
- **Verification:** 2026 → `HTTP 200`, 182 KB, `BEGIN:VCALENDAR`, **513 VEVENTs**. 2027 → `HTTP 200`, 160 KB, **455 VEVENTs**. Confirmed eclipses (e.g. 2027 `Annular solar eclipse`, `Total solar eclipse` Aug 2027), all major meteor showers, planetary oppositions, conjunctions, solstices/equinoxes.
- **Granularity fit:** VERY detailed → **too noisy at `maxdiff=7`** (500+ events incl. minor asteroid oppositions and Moon–planet conjunctions). The `maxdiff` parameter controls how many events are included — use a low value and/or filter to the ~15-20 tentpoles per year (eclipses, major meteor peaks, solstices, best planetary oppositions, supermoons).
- **Legal/ToS:** Free to use/import; site permits embedding/downloading. Good for internal planning; credit appreciated.
- **Best use:** Treat as the **authoritative data source** behind a curated, yearly-refreshed tentpole calendar.

### 3. Launch Library 2 (The Space Devs) — API for rocket launches  ✅ RECOMMENDED (volatile launches — build a filtered feed)
- **Provider:** The Space Devs — `ll.thespacedevs.com` (the de-facto community aggregator behind most launch apps/sites)
- **API base:** `https://ll.thespacedevs.com/2.2.0/` · upcoming launches: `https://ll.thespacedevs.com/2.2.0/launch/upcoming/`
- **Official?** No (aggregator, not the launch providers themselves) but it is THE authoritative consolidated source and the same data most third-party launch ICS feeds are built from.
- **Price:** Free. **Rate limit: 15 requests/hour per IP** anonymously; free API key raises it. (`/api-throttle` endpoint reports usage.)
- **Update cadence:** Live JSON, continuously updated. You would **build your own .ics** from it.
- **Maintenance burden:** MEDIUM — this is not a ready-made .ics; requires a small script (tools/) to pull, filter, and emit an .ics. Because launch dates slip, **refresh frequently (e.g. weekly, or daily near a launch)**, not yearly.
- **Verification:** `HTTP 200`; `upcoming/` returned **364 upcoming launches** with clean structured fields: `name`, `net` (target time), `net_precision` (Second/Hour/Day/Month — tells you how firm the date is), `status` (e.g. "Go for Launch"), `lsp_name`, `mission`.
- **Granularity fit for tentpoles — CRITICAL FILTERING:** Raw feed is dominated by routine Starlink batches (multiple per week) — far too granular. Filter to notable missions only, e.g.:
  - Crewed flights (Crew Dragon, Starliner, Artemis/Orion)
  - Starship test/orbital flights
  - Major NASA/ESA science & planetary launches, new-vehicle debuts, high-profile payloads
  - Use `net_precision` (prefer Day/Hour/Second) and `status` = Go to avoid pinning speculative dates.
- **Volatility flag:** Launch `net` dates change constantly. Label these events "target date — subject to change" and re-pull before relying on them.
- **Legal/ToS:** Data is free and open to everyone; attribution to The Space Devs expected. No paywall for this scale of use. (Consider a small monthly donation / API key for production reliability.)

---

## REJECTED / UNVERIFIED OPTIONS

| Option | Why not recommended |
|---|---|
| **github.com/vrachieru/astronomy-calendar** (`astronomy-calendar.ical`) | Fetched OK (`HTTP 200`, VCALENDAR, 919 VEVENTs, does contain 56 events in 2026 / 57 in 2027, sourced from seasky.org). BUT it is a **static file in a personal repo originating in 2015** — updates depend entirely on the maintainer manually committing. No auto-roll, high staleness risk. Not maintenance-free. Use seasky.org/in-the-sky as the live source instead. |
| **SmartCalendars.ai** (spacex-launches / nasa-launches feeds) | Ready-made ICS built on Launch Library 2 data, but the exact subscription URL is JavaScript-rendered and **could not be retrieved/verified**, and its SpaceX feed includes every Starlink launch (too granular for tentpoles). Third-party dependency. UNVERIFIED → not recommended; go direct to LL2 instead. |
| **spacexnow.com/integrations** | Page loads (`HTTP 200`) but the ICS/webcal URL is JS-rendered and **could not be extracted or verified**; site appears possibly stale. UNVERIFIED. |
| **NASA SKYCAL** (eclipse.gsfc.nasa.gov/SKYCAL) | Authoritative NASA sky-events data, but it **generates an .ics on demand via a web form** — there is no stable auto-updating subscription URL to point a calendar at. Good as a cross-check data source, not as a feed. |
| **NASA launch ICS feeds** | No official NASA-hosted auto-updating .ics launch subscription was found/verified. NASA launch data flows into LL2 anyway. |

---

## FINAL RECOMMENDATION

Use a **two-track approach**, matching maintenance to volatility:

**Track A — Stable astronomical tentpoles (eclipses, meteor peaks, solstices/equinoxes, supermoons):**
- **Simplest (zero maintenance):** subscribe to **`https://cantonbecker.com/astronomy-calendar/astrocal.ics`** and filter out moon-phase/retrograde noise when importing. Verified live, auto-rolling, free.
- **Most authoritative (recommended for the client who "cares deeply about accuracy"):** build a **curated, yearly-refreshed** tentpole calendar from **in-the-sky.org** (`newscalyear_ical.php?year=YYYY`), filtered to ~15–20 marquee events/year. Verified live. One-line yearly `year=` bump.
- These events are computed years ahead — safe to schedule promotions against now. In-window anchors already confirmed: **Total Solar Eclipse 12 Aug 2026** (Arctic→Greenland→Iceland→Spain), **Perseids peak ~12–13 Aug 2026**, **Geminids** (Dec), **Quadrantids** (early Jan 2027), solstices/equinoxes, and the **2 Aug 2027 total solar eclipse** on the horizon.

**Track B — Volatile launches (major missions only):**
- **Build a custom filtered .ics from Launch Library 2** (`ll.thespacedevs.com/2.2.0/launch/upcoming/`) via a small tool, **refreshed weekly**. Include only notable missions (crewed flights, Artemis/Orion, Starship flights, major NASA/ESA science launches) — exclude routine Starlink batches. Use `net_precision` + `status` to avoid speculative dates, and label every launch "target date — subject to change."

**Bottom line:** No single official auto-updating .ics covers both cleanly. Best result = cantonbecker (or curated in-the-sky) for the predictable astronomy tentpoles + a lightweight LL2-powered custom feed for the handful of headline launches, refreshed often because launch dates move.

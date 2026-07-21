# Motorsport — Tentpole Calendar Feed Research

**Category:** Motorsport
**Prepared for:** Pyros content-planning "tentpole" calendar
**Date:** 2026-07-21
**Target window:** now → rolling ~12 months (Jul 2026 → Jul 2027)
**Goal:** Correct, low/zero-maintenance public .ics feeds at *tentpole* granularity (one entry per marquee race weekend, not per practice/qualifying session).

All feeds below were **actually fetched and verified** (HTTP status + `BEGIN:VCALENDAR` + `VEVENT` count + sample events) unless explicitly marked UNVERIFIED.

---

## ✅ VERIFIED — RECOMMENDED

### 1. Formula 1 — race-only feed (BEST; zero maintenance, perfect granularity)

- **Provider:** f1calendar.com / motorsportcalendars (open-source project `sportstimes/f1`, the de-facto community-standard F1 calendar)
- **Feed URL (races only):** `https://files-f1.motorsportcalendars.com/f1-calendar_gp.ics`
  - Subscribe form: `webcal://files-f1.motorsportcalendars.com/f1-calendar_gp.ics`
- **Official?** No (community project), but sourced from the FIA-confirmed schedule and treated as the reference feed across the F1 community.
- **Price:** Free
- **Update cadence:** Auto — the CDN file is the "current season" feed and regenerates as the schedule is confirmed/changes; rolls over to the next season automatically each year.
- **Maintenance burden:** **None.** Subscribe once.
- **Granularity:** **Exactly tentpole** — one all-day/weekend event per Grand Prix. `SUMMARY` format: `F1: Grand Prix (Monaco Grand Prix)`.
- **Verification (2026-07-21):** HTTP 200, `BEGIN:VCALENDAR`, `PRODID:f1calendar.com`, **22 VEVENTs**, one per round, 2026-03-08 → 2026-12-06. Confirmed marquee events present: Monaco, British, Italian (Monza), Singapore, Miami, **Las Vegas**, **Abu Dhabi (season finale)**.
- **Notes:** Feed reflects the currently published season. If you want a granular version, the same project also serves per-session feeds (filename encodes sessions, e.g. `fp1_fp2_fp3_qualifying_sprintQualifying_sprint_gp`) — **not needed** for tentpole planning. The `_gp.ics` race-only file is the right one.
- **ToS/legal:** Free public project, MIT-licensed codebase; no auth, no scraping. Fine for internal planning.

---

## ✅ VERIFIED — USABLE WITH CAVEATS (non-F1 series)

Source: **toomuchracing.com/calendar** ("I Watch Too Much Racing") — a long-running hobbyist who publishes one **public Google Calendar** per series. Hosting is Google (very reliable); curation is a single volunteer.

**Shared caveat for ALL of these:** they are **multi-year archives** (hundreds of past events going back a decade), granularity is **inconsistent** (mix of per-round and per-session, plus support series like Indy NXT / ALMS mixed in), and event titles are hand-typed (typos, sponsor-name drift). They are auto-updating and free, but **cluttered** — not clean tentpole feeds. Recommend only if you want auto-update and will filter, otherwise prefer the curated approach below.

| Series | Verified feed URL (Google public .ics) | HTTP | VEVENTs | Tentpole example present |
|---|---|---|---|---|
| MotoGP | `https://calendar.google.com/calendar/ical/832vbii8pmrvma356b4vn3v42c%40group.calendar.google.com/public/basic.ics` | 200 | 451 | per-round rounds (R1…R22) + sprints |
| IndyCar | `https://calendar.google.com/calendar/ical/4lrug7rrj92k8f9n2svn2fm2qo%40group.calendar.google.com/public/basic.ics` | 200 | 270 | Indy 500 window (mixed w/ Indy NXT) |
| WEC (Le Mans) | `https://calendar.google.com/calendar/ical/61jccgg4rshh1temqk0dj4lens%40group.calendar.google.com/public/basic.ics` | 200 | 142 | `FIA WEC \| 24 Hours of Le Mans` (single event ✔) |
| NASCAR Cup | `https://calendar.google.com/calendar/ical/db8c47ne2bt9qbld2mhdabm0u8%40group.calendar.google.com/public/basic.ics` | 200 | 679 | per-race (Daytona 500 etc.) |
| IMSA | `https://calendar.google.com/calendar/ical/njulhksvo83qeoruc3nhend9js%40group.calendar.google.com/public/basic.ics` | 200 | 210 | `Rolex 24 At Daytona`, `Petit Le Mans` (single events ✔) |

All verified 2026-07-21: HTTP 200, valid `VCALENDAR`, current-season events present in the Jul 2026–Jul 2027 window.
(Also available on the same page: F2, F3, Formula E, WorldSBK, ELMS, DTM, GT World Challenge, Supercars, BTCC, WRC, NHRA, etc.)

---

## ✅ VERIFIED — MULTI-SERIES (single feed, but too granular)

### GitHub `Bmorganqwe98/racing-2026-calendar`

- **Feeds (verified 200, valid VCALENDAR):**
  - F1: `https://Bmorganqwe98.github.io/racing-2026-calendar/f1.ics` (110 VEVENTs — per session)
  - Combined: `https://Bmorganqwe98.github.io/racing-2026-calendar/racing-2026.ics` (288 VEVENTs — F1+F2+WEC+IMSA+IndyCar+WRC)
  - plus `f2.ics`, `wec.ics`, `imsa.ics`, `indycar.ics`, `wrc.ics`
- **Rejected for tentpole use:** per-session granularity (F1 alone = 110 events), and **fixed to the 2026 season** (filename/repo is `racing-2026`), so it needs a manual repo swap each year — a single hobbyist, real maintenance/continuity risk. Good hosting (GitHub Pages), correct track-local timezones.

### Better F1 Calendar
- `webcal://better-f1-calendar.vercel.app/api/calendar.ics` — verified 200, valid VCALENDAR, **70 VEVENTs** (per-session: Practice/Sprint/Qualifying/Race). Clean titles (`F1 British GP - Qualifying`) but too granular for tentpole; F1 race-only feed above is better.

---

## ❌ REJECTED / UNVERIFIED

- **calendar.formula1.com (official F1)** — Official F1 does publish a "download/sync" calendar, but the sync path is device-app driven and I did not retrieve a plain public `.ics` subscription URL to verify. Also per-session (every FP/Q/Sprint). **UNVERIFIED as a public feed; not recommended** — the community `f1-calendar_gp.ics` is cleaner and confirmed live.
- **MotoGP official (ECAL-powered) / IndyCar official (indycar.ecal.com)** — Official, but ECAL feeds are **account/selection-based personalized subscription URLs**, typically per-session, and I could not retrieve a stable anonymous `.ics`. **UNVERIFIED; not recommended** for a shared team feed.
- **motorsportcalendars.com hub** — Currently a "Coming Soon" placeholder. No feeds served. (Its F1 sub-property `files-f1.motorsportcalendars.com` IS the live F1 CDN recommended above.)
- **motorsport-calendars.com / rushsync.com / racingnews365 / calendarlabs** — pages found, but no plain public `.ics` subscription URL retrieved/verified from them. Not recommended without verification.
- **allseats.com MotoGP (`webcal://allseats.com/cal-event-4291.ics`)** — surfaced in search; **not fetched/verified**. Do not use.
- **romanzipp / nixxo / motogpcal.com MotoGP generators** — generator tools; no stable pre-built feed verified. Not recommended.

---

## ⭐ FINAL RECOMMENDATION

**Two-track approach:**

**1. Formula 1 → subscribe to the verified race-only feed (do this now).**
`https://files-f1.motorsportcalendars.com/f1-calendar_gp.ics`
Zero maintenance, exact tentpole granularity (one entry per Grand Prix), all marquee weekends present (Monaco, British/Silverstone, Monza, Singapore, Las Vegas, Abu Dhabi finale). This is the single best asset in the category and F1 is the most promotable series.

**2. All other motorsport marquee events → custom curated, yearly-refreshed calendar (~8–12 hand-picked entries).**
No clean *tentpole-only* multi-series feed exists: the auto-updating options (toomuchracing Google feeds) are cluttered multi-year archives with mixed granularity and support-series noise; the single-feed GitHub option is per-session and hard-coded to one season. For a promo calendar you only want a handful of anchors, so curate them once a year from authoritative sources:

| Event (tentpole) | Series | Authoritative source for the annual refresh |
|---|---|---|
| Daytona 500 (season opener) | NASCAR Cup | nascar.com |
| Rolex 24 At Daytona | IMSA | imsa.com |
| Indianapolis 500 | IndyCar | indycar.com |
| 24 Hours of Le Mans | FIA WEC | fiawec.com |
| Petit Le Mans | IMSA | imsa.com |
| MotoGP marquee rounds (e.g. Le Mans, Mugello/Italian, British, Valencia finale) | MotoGP | motogp.com |

For that curation you can pull dates directly from the **verified toomuchracing per-series feeds above** (WEC/IMSA already list Le Mans / Rolex 24 / Petit Le Mans as single events) or the series' official sites, then place ~8–12 anchor events into the team calendar. Budget ~30 min/year to refresh.

**Bottom line:** F1 is solved with a zero-maintenance official-grade feed. Everything else is best handled as a small curated yearly refresh rather than subscribing to noisy multi-series feeds.

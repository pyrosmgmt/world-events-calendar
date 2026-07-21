# Entertainment & Pop Culture — Tentpole Calendar Feed Research

**Category:** Entertainment & Pop Culture (award shows + major movie/streaming releases)
**Prepared for:** Pyros content-planning "tentpole" calendar
**Date:** 2026-07-21
**Target window:** now → rolling ~12 months (through ~mid-2027)
**Granularity target:** marquee moments only (Oscars, Grammys, Emmys, VMAs, Met Gala, blockbuster premieres) — NOT per-episode.

---

## TL;DR

There is **no single official, zero-maintenance .ics feed** covering this whole category. The landscape splits in two:

1. **Award shows** — one genuinely live, auto-updating third-party feed exists and is verified (CalendarX / AddEvent). Good tentpole granularity, free, low maintenance, but forward coverage is thin right now and has some placeholder-date noise, so dates must be spot-checked.
2. **Movie & streaming releases** — every dedicated .ics feed found is **dead or empty** (abandoned 2014–2022). Recommend building a **yearly-refreshed curated feed** seeded from the **TMDB API** (movies) plus manual curation of the handful of blockbuster/streaming tentpoles.

---

## VERIFIED OPTIONS (fetched live, confirmed real iCalendar)

### 1. Award Season Calendar — CalendarX (served via AddEvent) ✅ RECOMMENDED for award shows

| Field | Detail |
|---|---|
| Provider | CalendarX (calendarx.com), feed hosted on AddEvent.com |
| Feed URL (HTTPS) | `https://www.addevent.com/feed/eeeuadduw.ics` |
| Feed URL (webcal) | `webcal://www.addevent.com/feed/eeeuadduw.ics` |
| Landing page | https://www.calendarx.com/schedule/award-season-calendar |
| Official? | No — third-party aggregator (no official awards-body feed exists) |
| Price | Free |
| Update cadence | Auto-updating; feed declares `REFRESH-INTERVAL / X-PUBLISHED-TTL: PT2H` (2h). Content updated by CalendarX as dates are announced. |
| Maintenance burden (us) | Low — we subscribe once; they maintain content. |
| Reliability | Moderate. See caveats below. |
| Granularity | Excellent fit — pure award-show tentpoles, one entry per ceremony. |
| Legal/ToS | Free public subscription calendar; fine for internal planning. Don't scrape/redistribute wholesale. |

**Verification evidence (HTTP 200, `text/calendar`, 61.7 KB, 42 VEVENTs):**
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AddEvent.com v1.0//EN
NAME:Award Season Calendar
X-WR-CALNAME:Award Season Calendar
X-PUBLISHED-TTL:PT2H
REFRESH-INTERVAL;VALUE=DURATION:PT2H
```

**How the feed URL was found:** The landing page renders an AddEvent "subscribe to calendar" widget (`class="addeventstc" data-id="yy9g6wwb4pfp"`). The `+google` subscribe variant redirects to `...cid=http://www.addevent.com/feed/eeeuadduw.ics`, which is the underlying public ICS. That URL was fetched directly and confirmed as valid iCalendar.

**Sample events in feed (verified):** Primetime Emmy Awards, Grammy Awards, Golden Globe Awards, Academy Awards (Oscars), BAFTA Film Awards, SAG Awards, Critics Choice, Tony Awards, BET Awards, MTV VMAs, ESPY Awards, The Game Awards, Daytime Emmys, ACM Awards, NAACP Image Awards.

**⚠️ Caveats (important for the accuracy-sensitive client):**
- **Thin forward coverage right now.** As of 2026-07-21, only 2 events fall inside our target window: *MTV VMAs 2026 (Sep 6)* and *Primetime Emmy Awards 2026 (Sep 14)*. The bulk of the 42 events are the just-finished 2025–26 season. The 2026–27 season (Grammys Feb '27, Oscars ~March '27, Golden Globes Jan '27, etc.) is **not yet populated**, presumably because the aggregator adds them as official dates firm up. This should refresh over the season, but it means the feed alone will not fill a 12-month planner today.
- **Placeholder-date noise.** ~30 events are dumped on a single date (2026-04-29) — clearly "date TBD" placeholders (e.g. multiple "Oscar Voting", guild awards, "The Game Awards"). Any date pulled from this feed must be cross-checked before it drives a promo.
- **No Met Gala** in the current feed (Met Gala is first Monday of May — worth adding manually; it's a huge pop-culture tentpole for this audience).

---

## REJECTED / UNVERIFIED OPTIONS

### Movie release .ics feeds — all DEAD

| Provider | URL | Verified result | Verdict |
|---|---|---|---|
| XerBlade "Comic Book Superhero Movies" (public Google Calendar) | `https://calendar.google.com/calendar/ical/qeklju8c6bjke09o50jrk3p544%40group.calendar.google.com/public/basic.ics` | HTTP 200, valid VCALENDAR, 58 events — **but last event is 2022-05-06.** Abandoned. | ❌ Stale |
| Kouzos Movie Releases | `webcal://www.kouzos.com/ical/Movies.ics` | HTTP 200, valid VCALENDAR, 105 events — **but newest events are 2014–2015.** Abandoned. | ❌ Stale |
| Kouzos DVD Releases | `webcal://www.kouzos.com/ical/DVD.ics` | Same abandoned service. | ❌ Stale |

### Streaming (Netflix) .ics feeds — empty / not zero-maintenance

| Provider | URL | Verified result | Verdict |
|---|---|---|---|
| CalendarLabs "Netflix Calendar" | `https://www.calendarlabs.com/ical-calendar/ics/subscribe/711/Netflix_Calendar` | HTTP 200 but returns **HTML, 0 VEVENTs**; page literally says "No Events Found." | ❌ Empty/abandoned |
| Smart Calendars AI (Netflix regional feeds) | smartcalendars.ai/en/feeds/... | Not fetched/verified. Even if live, Netflix feeds list **every title** → too granular for a tentpole calendar. | ❌ Wrong granularity / unverified |
| fabsrc/netflix-release-cal (GitHub) | github.com/fabsrc/netflix-release-cal | Self-host project — requires us to deploy & run it. Not zero-maintenance. | ❌ Not turnkey |

### Award-show alternatives considered (no feed)

| Provider | Notes | Verdict |
|---|---|---|
| Outside.so /awards | Confirms 2026–27 award dates exist and are public (VMAs, Emmys, Game Awards, Golden Globes, Critics Choice, People's Choice, Grammys, BAFTA, Spirit Awards, Oscars all listed with countdowns). **App-only — no .ics subscription.** Useful as an authoritative cross-check source. | Reference only, not a feed |
| Deadline / Hollywood Reporter / Variety / Primetimer "Awards Season Calendar" articles | Authoritative human-curated date lists, updated each season. No .ics. | Best data source for curation |

---

## MOVIE / STREAMING TENTPOLES — recommended data source (no live feed exists)

Since no maintained .ics feed exists for movies/streaming, build a **custom yearly-refreshed feed**:

**Primary source — TMDB API (The Movie Database), free with API key:**
- Upcoming list: `GET https://api.themoviedb.org/3/movie/upcoming?region=US`
- Exact dated release types: `GET https://api.themoviedb.org/3/movie/{movie_id}/release_dates`
- Discover with filters (by date range, popularity, region): `GET https://api.themoviedb.org/3/discover/movie`
- Docs: https://developer.themoviedb.org/reference/movie-upcoming-list
- Approach: pull upcoming US theatrical releases, filter to **high-profile only** (major franchises / high popularity score / wide release) so we get tentpoles, not every indie. Refresh 1–2×/year.
- ToS note: TMDB API is free but requires attribution and an API key; fine for internal use.

**Secondary sources for cross-checking dates:** Box Office Mojo release calendar (boxofficemojo.com/calendar), studio announcements. For streaming, curate manually from "What's on Netflix / Coming Soon" and trade press — only the 3–6 genuinely huge season drops per year (e.g. Stranger Things-tier), never per-episode.

---

## FINAL RECOMMENDATION

**Hybrid: one live feed for awards + a curated yearly-refresh layer for movies/streaming.**

1. **Award shows → SUBSCRIBE to the verified CalendarX/AddEvent feed:**
   `https://www.addevent.com/feed/eeeuadduw.ics` (webcal: `webcal://www.addevent.com/feed/eeeuadduw.ics`)
   - Zero ongoing effort, auto-updating, correct tentpole granularity.
   - **But** treat it as a feeder, not gospel: verify each date against Deadline/THR/Variety's awards-season calendar (or Outside.so) before it drives a promo, and manually add the **Met Gala** (first Monday of May) which the feed omits. Re-check in fall 2026 that the 2026–27 season has populated.

2. **Movies & streaming → build a custom, yearly-refreshed curated calendar** seeded from the **TMDB API** (movie release dates, filtered to blockbusters) plus a short hand-picked list of marquee streaming premieres. No reliable maintained public .ics feed exists for this — every candidate found was dead (XerBlade 2022, Kouzos 2015) or empty (CalendarLabs Netflix).

**Key tentpole events to guarantee are in the final calendar (12-mo window):**
Academy Awards (Oscars), Grammys, Primetime Emmys, Golden Globes, Met Gala, MTV VMAs, SAG Awards, BAFTA, Critics Choice, People's Choice, Tony Awards, BET Awards, The Game Awards + a curated shortlist of major blockbuster theatrical releases (Marvel/DC/franchise, via TMDB) and the 3–6 biggest streaming season premieres.

**Authoritative sources for the yearly curation refresh:** TMDB API (movies), Deadline / Hollywood Reporter / Variety awards-season calendars (award dates), Box Office Mojo (release dates), Outside.so (award-date cross-check).

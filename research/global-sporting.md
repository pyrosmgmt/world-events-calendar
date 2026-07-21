# Global Sporting Events — Calendar Feed Research

**Category:** Global Sporting Events (tentpole / mega-events only)
**Prepared:** 2026-07-21
**Goal:** One entry per tournament (e.g. "FIFA World Cup 2026", "Olympic Games", "UEFA Euro"), spanning its dates — NOT every fixture. Prefer correct, low/zero-maintenance public `.ics` feeds.
**Target window:** 2026-07-21 → ~2027-07 (rolling 12 months).

---

## TL;DR

There is **no official, aggregated, tentpole-granularity `.ics` feed** for global sporting mega-events. FIFA, the IOC, UEFA, ICC and World Rugby do **not** publish public iCalendar subscriptions of their headline events. Third-party feeds exist and several are live and valid, but they are either (a) far too granular (per-match / per-race) or (b) unofficial with unknown longevity and no clear ToS.

**Recommendation: build a small CUSTOM curated calendar (one entry per tentpole, refreshed yearly), seeded from `sporting-events.org` + Wikipedia and verified against each governing body.** Optionally subscribe to a couple of `sporting-events.org` per-sport feeds as a live cross-check. Details and reasoning below.

---

## Verified options (fetched live, confirmed real iCalendar)

### 1. sporting-events.org — per-sport feeds (BEST available live feeds, but imperfect granularity)
- **Provider:** sporting-events.org ("Every Major Sporting Event"), independent UK-style aggregator. Has `/about/` and `/contact/` pages only — **no published Terms of Service or licensing statement**.
- **Verification:** HTTP `200`, `Content-Type: text/calendar`, valid `BEGIN:VCALENDAR` with `PRODID:-//sporting-events.org//SE Feeds 1.0//EN`. Confirmed live on 2026-07-21.
- **Official?** No.  **Price:** Free.  **Cadence:** Live subscription; calendar apps refresh on their own schedule. Site maintains it manually (dates/fixtures appear pre-loaded).
- **Feed URLs (all confirmed live, `text/calendar`, contain VEVENTs):**

| Feed | URL | VEVENTs | Granularity |
|---|---|---|---|
| All events | `https://sporting-events.org/feeds/all.ics` | 1000 (capped) | ❌ Too granular — individual F1 GPs, UFC nights, tennis opens, single Tour stages |
| FIFA World Cup | `https://sporting-events.org/feeds/fifa-world-cup.ics` | 4 | ⚠️ Only semis/3rd-place/final — no whole-tournament entry |
| Champions League | `https://sporting-events.org/feeds/champions-league.ics` | 3 | ⚠️ Matchday/round rows, not one entry |
| Cricket | `https://sporting-events.org/feeds/cricket.ics` | 15 | ⚠️ Mix of tournaments + individual series/tests |
| Rugby Union | `https://sporting-events.org/feeds/rugby-union.ics` | 21 | ❌ Mostly individual matches |
| Six Nations | `https://sporting-events.org/feeds/six-nations.ics` | 3 | ⚠️ Per-round |
| Winter Sports | `https://sporting-events.org/feeds/winter-sports.ics` | 4 | ✅ Tournament-level (World Championships) |

  Other confirmed per-sport feeds on the same pattern (`/feeds/<slug>.ics`): `football`, `premier-league`, `nba`, `nfl`, `motorsport`, `tennis`, `golf`, `wimbledon`, `the-masters`, `athletics`, `baseball`, `basketball`, `horse-racing`, `american-football`.

- **Evidence snippet (all.ics):**
  ```
  X-WR-CALNAME:Major Sporting Events Calendar – Sporting Events
  SUMMARY:2026 Tour de France Final Stage   (DTSTART;VALUE=DATE:20260726)
  SUMMARY:Hungarian Grand Prix              (DTSTART;VALUE=DATE:20260724)
  SUMMARY:FIFA World Cup 2026 Final         (fifa-world-cup.ics)
  ```
- **Maintenance burden:** Zero if subscribed as-is. **BUT** does not meet the tentpole requirement cleanly: `all.ics` is far too granular (individual matches/races), and per-sport feeds mix tournament- and match-level rows. Reliability/longevity unproven; a solo-run aggregator could disappear. No ToS.
- **Verdict:** Excellent **seed/reference source** and usable as a live cross-check. Not a drop-in tentpole feed.

---

## Rejected / unverified options

### CalendarLabs — FIFA World Cup feed → REJECTED (broken/empty)
- URL tested: `https://www.calendarlabs.com/ical-calendar/ics/196/FIFA_World_Cup.ics`
- Result: HTTP `200`, `Content-Type: text/calendar`, but **0 bytes / 0 VEVENTs** — empty response. Not usable. Listing pages are JS-rendered and expose no scrapable `.ics` links.

### matchcalendar.football / worldcupcalendar.football / wc26cal.com / football-calendar.com → NOT FIT (per-match)
- These provide FIFA World Cup 2026 feeds but at **per-match (104 matches) granularity**, with per-team/per-group/per-city variants. Great for fans, wrong altitude for a tentpole promo calendar. Not individually fetch-verified because granularity already disqualifies them.

### thatbritguy/world-cup-ics (GitHub) → NOT FIT (per-match)
- Auto-updating GitHub-hosted `.ics` for the FIFA World Cup, per-match. Same granularity mismatch.

### Official governing-body feeds → DO NOT EXIST as .ics
- **IOC Olympics** (`https://www.olympics.com/ioc/event-calendar`): page fetched — **no `.ics` feed present**. Human-readable only.
- **FIFA, UEFA, ICC, World Rugby, ASO (Tour de France), Commonwealth Games Federation:** none publish a public tentpole `.ics` subscription (as of this research). Schedules are published as web pages / PDFs.

---

## Window note (important)
Today is **2026-07-21**. The forward 12-month window means several "obvious" mega-events are actually **just past**: FIFA World Cup 2026 (Jun 11–Jul 19 2026) has concluded; Winter Olympics Milan-Cortina (Feb 2026) is past; the next Summer Olympics is **LA 2028** (outside the window). In-window tentpoles skew toward: closing of the 2026 Tour de France, cricket tours/ICC events, Rugby "Nations Championship" (Nov 2026), Six Nations 2027 (Feb–Mar 2027), 2027 Winter World Championships (ski/biathlon/figure skating), and domestic league finals (UCL final ~late May 2027). Confirm the exact tentpole list against the window at build time.

---

## FINAL RECOMMENDATION

**Build a custom, curated, yearly-refreshed "Global Sporting Tentpoles" calendar** — one all-day (or multi-day) VEVENT per mega-event spanning its full run. This is the only way to guarantee correct tentpole granularity, and the maintenance is genuinely light: a global-sports mega-event list changes only a handful of times a year and dates are known far in advance.

**Why not a live feed:** no official tentpole `.ics` exists; the one broad third-party feed (`sporting-events.org/feeds/all.ics`) is capped at 1000 rows of match/race-level noise; the CalendarLabs event feed is broken. None satisfy "one entry per tournament."

**Suggested build (fits the WAT framework — a yearly tool + workflow):**
1. **Seed** the list from two already-aggregated sources, then verify each date against the governing body:
   - `sporting-events.org` per-sport feeds (live, free, valid — good structured seed).
   - Wikipedia "2026 in sports" / "2027 in sports" year pages (comprehensive, well-sourced).
2. **Authoritative per-event sources to verify against:**
   - FIFA — `fifa.com` (World Cup, Club World Cup)
   - IOC — `olympics.com/ioc/event-calendar` (Olympics, Youth Olympics)
   - UEFA — `uefa.com` (Champions League final, Euro)
   - ICC — `icc-cricket.com` (Cricket World Cup / T20 World Cup)
   - World Rugby — `world.rugby`; Six Nations — `sixnationsrugby.com`
   - ASO — `letour.fr` (Tour de France)
   - Commonwealth Games Federation — `thecgf.com`
3. **Output** a single hand-maintained `.ics` (or a Google Calendar the team subscribes to), regenerated ~once a year plus ad-hoc when a major date is confirmed/moved.

**Effort:** ~1–2 hours to build the initial 15–30 tentpole entries; ~30 min/year to refresh. This beats babysitting an unofficial feed of unknown longevity, and guarantees the accuracy the client requires.

**Cross-check option (low effort):** additionally subscribe the planning calendar to `sporting-events.org/feeds/winter-sports.ics` (cleanly tournament-level) and glance at `all.ics` when planning, as a free live prompt so no big event is missed — but treat it as a hint, not the source of truth.

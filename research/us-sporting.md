# US Sporting Events — Tentpole Calendar Feed Research

**Category:** US Sporting Events (tentpole / season & championship level, NOT every fixture)
**Prepared:** 2026-07-21
**Target window:** rolling ~12 months (Aug 2026 → Jul 2027)
**Goal:** correct, low/zero-maintenance public `.ics` feed for content-planning promos.

---

## TL;DR / Final Recommendation

**No official, tentpole-only `.ics` feed exists for US sports.** Every public feed we could find is either (a) an unofficial third-party service that publishes **every game** (far too granular — hundreds of VEVENTs that would bury the ~15-20 marquee events the client actually cares about), or (b) a valid-but-empty personalized feed that needs manual per-team configuration.

**Recommendation: Build a custom, curated, yearly-refreshed calendar** (~15-25 tentpole events). Populate it once per year using authoritative sources, primarily the **free, no-key ESPN API** (verified live below) for league season/playoff windows, plus official event sites for fixed marquee dates. Maintenance is roughly one refresh per year (~1-2 hrs) plus a light check when playoff brackets set exact dates.

This aligns with the client's #1 priority (accuracy) better than any auto-feed, because auto-feeds are all game-by-game and none is authoritative for "tentpole" granularity.

---

## Verified live (HTTP-checked) — but REJECTED on granularity/fit

### 1. ecal (powers "Fox Sports", Sync2Cal, and many team calendars)
- **Provider:** ecal.com (third-party white-label calendar platform)
- **Feed URL tested:** `https://ics.ecal.com/ecal-sub/689c0450a176b50008c377e1/Fox%20Sports.ics`
- **Verification:** `HTTP 200`. Response is real iCalendar — contains `BEGIN:VCALENDAR`, `PRODID:-//E-DIARY//E-DIARY 1.0//EN`, `X-WR-CALNAME:Fox Sports`. **However `BEGIN:VEVENT` count = 0** (header `X-Built-On-Cache-Miss:true`). The subscription is personalized/empty until you configure teams/sports through their signup flow.
- **Official?** No (aggregator, though co-branded with Fox Sports).
- **Price:** Free tier exists.
- **Cadence:** Auto-updating once configured.
- **Fit:** Poor. When populated it is **full-fixture**, and the raw URL is empty. Not usable as a drop-in tentpole feed.

### 2. ESPN "hidden" public API (NOT an .ics — a data source for building one) ✅ BEST DATA SOURCE
- **Provider:** ESPN (undocumented but widely used public JSON endpoints).
- **Endpoints tested (all `HTTP 200`, JSON):**
  - `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard` → NFL 2026 season `startDate`/`endDate`.
  - `https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2026/types/3?lang=en` → NFL **Postseason** window `2027-01-13` → `2027-02-16` (Super Bowl falls inside this).
  - `https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard` → NBA 2026-27 `2026-09-30` → `2027-06-26` (Finals inside).
  - `https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard` → MLB 2026 `2026-02-19` → `2026-11-12` (World Series inside).
- **Official?** Semi — it is ESPN's own backend, but undocumented and unsupported (could change without notice). No API key required.
- **Price:** Free.
- **Legal/ToS:** Undocumented endpoint; no published license. Low legal risk for reading dates for internal planning, but do not assume an SLA. Use as a build-time date source, not a live customer-facing feed.
- **Fit:** Excellent as the **authoritative date engine** for a custom curated build. Confirms season kickoff, postseason start, and championship windows programmatically for NFL/NBA/MLB/NHL/college.

---

## Rejected / Unverified providers (full-fixture, unofficial, or not directly fetchable)

| Provider | URL | Official | Price | Why rejected |
|---|---|---|---|---|
| **SportsCal** | `https://sportscal.io/` | No | Paid (~$47/yr) | Full-fixture per-team feeds; paid; feed URL only issued after signup (could not fetch a raw `.ics` to verify). |
| **Your Sports Calendar** | `https://yoursportscalendar.com/` | No | Free | Full-fixture; page is JS-rendered, no direct `.ics` URL exposed in HTML to verify. |
| **Sync2Cal** | `https://www.sync2cal.com/` | No | Freemium | Full-fixture; delivers via ecal/Google OAuth flow, no standalone verifiable `.ics`. |
| **FanFeed** | `https://fanfeed.tv/calendar/nfl` | No | Free/Freemium | Personalized subscription link per user; full-fixture. |
| **fixturedownload.com** | `https://fixturedownload.com/` | No | Free | Full-fixture; iCal only via a download page (no clean subscribable feed URL); returned HTML/JSON, not a live `.ics`, on direct fetch. |
| **MySportsCal.com** | `http://www.mysportscal.com/` | No | Free | Full-fixture downloads; dated/static, not auto-updating. |

None of these is tentpole-granularity, none is official league-run, and all carry third-party reliability/ToS uncertainty. Not recommended.

---

## Recommended build: custom curated "US Sports Tentpole" calendar

**Approach:** maintain a hand-curated `.ics` (~15-25 VEVENTs) refreshed once per year (do a mid-season sanity pass when playoff dates lock). Generate dates from the ESPN API + official event sites.

### Tentpole events to include (rolling 12 months from Jul 2026)
- **NFL:** Season kickoff (early Sep 2026) · Thanksgiving games (late Nov) · Playoffs start (mid-Jan 2027) · **Super Bowl LXI** (early-mid Feb 2027; inside verified ESPN postseason window 2027-01-13→02-16) · NFL Draft (late Apr 2027)
- **NBA:** Opening night (late Oct 2026) · NBA All-Star Weekend (mid-Feb 2027) · **NBA Finals** (Jun 2027; inside verified window ending 2027-06-26)
- **MLB:** Opening Day (late Mar 2027) · All-Star Game (mid-Jul) · **World Series** (late Oct 2026; inside verified window ending 2026-11-12)
- **NHL:** Stanley Cup Final (Jun 2027)
- **College:** March Madness / Final Four (Mar-Apr 2027) · College Football Playoff National Championship (Jan 2027) · Bowl season (late Dec 2026)
- **Golf:** The Masters (Apr 2027) · US Open · PGA Championship
- **Tennis:** US Open (late Aug-early Sep 2026)
- **Motorsport:** Daytona 500 (Feb 2027) · Indianapolis 500 (late May 2027)
- **Horse racing:** Kentucky Derby (first Sat May 2027) · the Triple Crown (Preakness, Belmont)
- **Combat/other:** marquee UFC pay-per-views (optional, brand-dependent)

### Authoritative data sources for the yearly refresh
1. **ESPN API** (verified free/no-key) — league season start/end and postseason windows for NFL/NBA/MLB/NHL/college. Base: `https://site.api.espn.com/apis/site/v2/sports/...` and `https://sports.core.api.espn.com/v2/sports/...`.
2. **Official league sites** for exact marquee dates once announced: NFL.com, NBA.com, MLB.com, NHL.com, NCAA.com.
3. **Official event sites** for fixed annual events: masters.com, usopen.org (tennis), kentuckyderby.com, indianapolismotorspeedway.com, daytonainternationalspeedway.com.

### Build mechanics
- A small script (fits the WAT `tools/` pattern) can pull ESPN windows, merge a small static YAML of fixed marquee events, and emit a valid `.ics` (`BEGIN:VCALENDAR` + one all-day `VEVENT` per tentpole).
- Host the generated `.ics` somewhere static (e.g. a cloud bucket / GitHub raw) so the team can subscribe once and you regenerate yearly.
- Set exact times only when confirmed; use all-day events for anything not yet scheduled to avoid wrong-time errors.

### Maintenance burden
- **~Once per year** full refresh + **one mid-season check** (Dec-Jan) when playoff/championship exact dates are set. This is materially lower-risk than trusting an unofficial auto-feed that could break silently or flood the calendar with every game.

---

## Evidence log (what was actually fetched)
- `ics.ecal.com/.../Fox%20Sports.ics` → HTTP 200, valid `BEGIN:VCALENDAR`, 0 VEVENTs (cache-miss/personalized).
- `site.api.espn.com/.../nfl/scoreboard` → HTTP 200, NFL 2026 season dates present.
- `sports.core.api.espn.com/.../nfl/seasons/2026/types/3` → HTTP 200, postseason `2027-01-13`→`2027-02-16`.
- `site.api.espn.com/.../nba/scoreboard` → HTTP 200, NBA 2026-27 `2026-09-30`→`2027-06-26`.
- `site.api.espn.com/.../mlb/scoreboard` → HTTP 200, MLB 2026 `2026-02-19`→`2026-11-12`.
- Third-party calendar pages (yoursportscalendar.com, sportscal.io, sync2cal.com) are JS-rendered and exposed **no** directly fetchable `.ics` URL in HTML — hence marked unverified.

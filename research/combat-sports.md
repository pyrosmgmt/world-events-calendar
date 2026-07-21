# Combat Sports — Calendar Feed Research

**Category:** Combat Sports (UFC/MMA, boxing, crossover events)
**Use case:** Broad "tentpole" content-planning calendar for the Pyros team (one entry per marquee event/card, not per fight).
**Research date:** 2026-07-21
**Target window:** rolling ~12 months from today.
**Priority:** feeds that are CORRECT with little/no maintenance.

All `.ics` candidates below were fetched live and checked for `BEGIN:VCALENDAR` + `VEVENT` content. HTTP results and evidence snippets are recorded. Anything I could not retrieve is marked UNVERIFIED and is not recommended.

---

## ✅ VERIFIED FEEDS

### 1. UFC — `clarencechaan/ufc-cal` (GitHub) — RECOMMENDED for UFC/MMA
- **Provider:** Open-source project by Clarence Chan (GitHub), scrapes the official `ufc.com/events` page several times daily.
- **Subscription URL (webcal):** `webcal://raw.githubusercontent.com/clarencechaan/ufc-cal/ics/UFC.ics`
- **Direct HTTPS URL (verified):** `https://raw.githubusercontent.com/clarencechaan/ufc-cal/ics/UFC.ics`
- **Official?** No (unofficial, but sourced directly from ufc.com).
- **Price:** Free (public GitHub raw file).
- **Update cadence:** Auto — repo scrapes ufc.com several times per day; `X-PUBLISHED-TTL:PT1H`. DTSTAMP on fetch was `20260719T131145Z` (2 days old — actively maintained).
- **Maintenance burden:** ~Zero. Subscribe once; it self-updates. Only risk = maintainer abandons the repo or GitHub raw hosting changes.
- **Reliability:** High. Data traces back to the official UFC events page.
- **Granularity:** EXCELLENT fit — **one VEVENT per event/card** (both numbered PPVs and Fight Nights), not per individual fight. Full fight card is in the event DESCRIPTION.
- **Verification evidence:**
  - `HTTP 200`, `BEGIN:VCALENDAR` present, **23 VEVENT entries**.
  - `X-WR-CALNAME:UFC`, `PRODID:adamgibbons/ics`.
  - First events: `20260321 UFC Fight Night: Evloev vs Murphy`, `20260412 UFC 327: Prochazka vs Ulberg`.
  - Later events: `20260816 UFC 330: Makhachev vs Machado Garry`, `20260905 UFC Fight Night: TBD vs TBD` (rolls forward as UFC announces cards).
- **ToS/legal:** Unofficial scrape of ufc.com; personal/internal planning use only (do not resell). Not affiliated with UFC.

### 2. ONE Championship + UFC — `mmacalendars.com` (Richard Soper)
- **Provider:** `mmacalendars.com`, open-source (GitLab), pulls directly from `ufc.com/events` and `onefc.com/events`.
- **Verified direct URLs:**
  - UFC: `https://mmacalendars.com/ufc` — `HTTP 200`, `application/octet-stream`, `BEGIN:VCALENDAR`, **48 VEVENTs**.
  - ONE Championship: `https://mmacalendars.com/onefccalendar` — `HTTP 200`, `BEGIN:VCALENDAR`, **28 VEVENTs**.
  - Apple/Google helpers: `/ufc/apple`, `/ufc/google`, `/onefc/apple`, `/onefc/google`.
- **Official?** No (unofficial; sources are the official org events pages). **Price:** Free, ad-free, no trackers. **Cadence:** Auto (page footer showed "Last updated: 2026-07-20").
- **Granularity note:**
  - Their **UFC** feed splits each card into **two** entries — `Prelims - ...` and `Main Card - ...` (48 events ≈ 24 cards). That is **too granular** for a tentpole calendar → prefer the `clarencechaan` feed above for UFC.
  - Their **ONE Championship** feed is **one entry per event** (e.g. `ONE Fight Night 49`, `ONE SAMURAI 4`) → **good tentpole fit** and the best verified option if Pyros wants ONE Championship coverage.
- **Reliability:** High; open source and self-hostable (Docker image available) if the public instance ever goes down.

---

## ⚠️ REJECTED / UNVERIFIED

### Sync2Cal (`sync2cal.com/sports/fighting/boxing`, `/ufc`) — UNVERIFIED, account-gated
- Pages load (`HTTP 200`) but expose **no public raw `.ics`/`webcal` URL** in the HTML. Subscribing requires signing in with a Google/Apple/Microsoft account (10 "sign in" prompts on the boxing page; per-user OAuth feed). Free tier limits you to **one** fighting calendar.
- Because there is no retrievable public feed URL, I **cannot verify** the calendar contents → not recommended. Also adds a login/account dependency (maintenance + ToS friction) we want to avoid.

### PBC (`pbc.ecal.com`) / eCal boxing calendars — UNVERIFIED
- `HTTP 200` but the page is an eCal widget shell; **no public `.ics` URL exposed**. eCal feeds are typically generated per-user behind their widget/SDK, so nothing verifiable to subscribe to programmatically.

### AllSeats (`webcal://allseats.com/cal-event-6879.ics`) — NOT SUITABLE
- Ticketing-vendor feed tied to a **single event listing**, not a rolling schedule of all cards. Not a maintainable category feed.

### fights.guide — UNREACHABLE
- Connection dropped on fetch (`RemoteDisconnected`). No verifiable `.ics` obtained → not recommended.

### Boxing generally — NO reliable free official `.ics` found
- Boxing has **no single governing body/schedule** (multiple promoters: DAZN/Matchroom, Top Rank/ESPN, PBC, Riyadh Season, Queensberry, plus Misfits/KSI crossover on DAZN). No authoritative, auto-updating public `.ics` feed could be located and verified. Sync2Cal exists but is account-gated/unverifiable (above).

---

## 🎯 FINAL RECOMMENDATION

**1. UFC / MMA — subscribe to a live feed (zero maintenance):**
- **Primary (UFC, tentpole granularity):** `https://raw.githubusercontent.com/clarencechaan/ufc-cal/ics/UFC.ics`
  (webcal: `webcal://raw.githubusercontent.com/clarencechaan/ufc-cal/ics/UFC.ics`). Verified live, one entry per card, self-updating from ufc.com.
- **Optional add (ONE Championship):** `https://mmacalendars.com/onefccalendar` — verified, one entry per event.
- Both are unofficial-but-official-sourced and free. Treat as internal planning aids; expect card details (fighters) to shift — but the **event-exists-on-this-date** layer (what Pyros needs) is stable.

**2. Boxing + crossover (KSI/Misfits) — BUILD a custom curated, yearly-refreshed calendar.**
No trustworthy free official `.ics` exists for boxing. For a tentpole calendar we only need the handful of marquee cards per year, so a light curated approach is both feasible and more stable than any auto-scrape:
- **Authoritative data sources to populate it from:**
  - **ESPN Boxing Schedule** (`espn.com/boxing/story/_/id/12508267/boxing-schedule`) — broad, well-maintained.
  - **BoxRec** (`boxrec.com`) — the sport's system of record for bouts/dates.
  - **Tapology FightCenter** (`tapology.com/fightcenter`) — MMA + boxing upcoming events.
  - **Misfits Boxing / DAZN** (`misfitsboxing.com`, DAZN schedule) — for KSI/Misfits crossover cards.
- **Suggested cadence:** refresh quarterly (boxing announces marquee cards a few months out). Enter only tentpole cards (major title fights, marquee heavyweight bouts, big crossover events) as one all-day entry per event.
- This fits the existing WAT framework: a `tools/` script could pull ESPN/BoxRec and emit a curated `.ics`, refreshed on a schedule.

**Bottom line:** UFC/MMA is solved with a verified auto-updating feed and needs no upkeep. Boxing/crossover has no reliable feed and should be a small hand-curated, quarterly-refreshed calendar built from ESPN/BoxRec/Tapology (+ Misfits/DAZN for crossover).

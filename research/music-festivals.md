# Music & Festivals — Calendar Feed Research

**Category:** Music & Festivals (tentpole events for the Pyros content-planning calendar)
**Researched:** 2026-07-21
**Target window:** rolling ~12 months (Jul 2026 → Jul 2027)
**Granularity target:** one entry per major festival (spanning its dates), NOT per set.

---

## TL;DR / Final Recommendation

**No festival publishes an official, auto-updating `.ics` feed of its own dates.** (Coachella, Glastonbury, Tomorrowland, Ultra, Lollapalooza, EDC, Reading & Leeds all publish dates as web-page text only.)

The only live, free, auto-updating `.ics` feeds that exist for these festivals are **third-party AI-curated feeds from Smart Calendars AI**. They are technically valid and live — **but I verified they contain real, disqualifying accuracy errors** (a hallucinated golf "parking pass" event inside the Coachella feed, duplicate entries, wrong event durations, and false `[CANCELLED]` tags). For a client that "cares deeply about accuracy," these cannot be the source of record.

**➡️ RECOMMENDATION: Build a custom, curated, yearly-refreshed calendar** (~12–15 tentpole festivals), sourced from each festival's official site and cross-checked against Music Festival Wizard / Billboard. This is the reliable-and-low-maintenance path: festival dates change only once a year and are announced far in advance, so a single annual refresh (plus a mid-year check) keeps it correct. Optionally subscribe to the Smart Calendars AI feeds in a *staging* calendar purely as an early-warning signal for newly announced dates — never as the published source.

---

## VERIFIED FEEDS (fetched live, valid iCalendar)

All URLs below returned **HTTP 200** and valid `BEGIN:VCALENDAR` + `VEVENT` payloads on 2026-07-21. Provider is **Smart Calendars AI** (smartcalendars.ai), a commercial AI-calendar app. Feeds are **free, unofficial (AI-curated), auto-updating (REFRESH-INTERVAL 24h)**. Data is generated/curated by their AI from "official festival and ticketing sources" — accuracy is NOT guaranteed and errors were observed (see Rejected section).

| Festival | Feed URL (`.ics`) | Events | Notes / observed issues |
|---|---|---|---|
| Glastonbury | `https://smartcalendars.ai/cal/1bba9226328e107568e1e523a7fb84821aee1ed3874b12d60bc29663d9d83565.ics` | 2 (2026, 2027) | 2027 event is an all-day 23–27 Jun span; description admits dates are "reported," unconfirmed on official site. |
| Coachella | `https://smartcalendars.ai/cal/84d3992ea37fe95c0dd1f15df546fc049b47c077d6b316b1816c012543113b72.ics` | 4 | **Contains a hallucinated event** — "Parking Pass: Cadillac Championship" (a golf event) — plus a spurious "[CANCELLED]" entry. Weekend events are single-day, not 3-day spans. |
| EDC Las Vegas | `https://smartcalendars.ai/cal/185205795c637f397ce7b840941f8124dd2991e6e343819edb6e26b0559435f6.ics` | 2 | 2026 falsely tagged `[CANCELLED]`; 2027 encoded as one 12-day span (conflates the two Dusk/Dawn weekends). |
| Bonnaroo | `https://smartcalendars.ai/cal/1ad95b6654934adb34b9b9e0611cd59015b0440349d7e1847f38524efbc3eff0.ics` | — | Live, valid VCALENDAR. |
| Download (UK) | `https://smartcalendars.ai/cal/4aa786bd78ef14b7698bd4c9968db0cd5bfb6b595f57938f3a1d844ba720a04a.ics` | 1 | Live, valid VCALENDAR. |
| Austin City Limits | `https://smartcalendars.ai/cal/9334401f391ee954b1c579db663f20c425c06fc0eb8da6b6aa96bce66c6dcfd1.ics` | 4 | Live, valid VCALENDAR. |
| **US all-festivals aggregate** | `https://smartcalendars.ai/cal/6902abc3c1b70e58fb69a269f757617a557eb6ed09a7c27964e3c6f144998018.ics` | 61 | One feed, many festivals. **But too granular + duplicated** — Coachella appears 3× under different names; includes dozens of minor/jazz/country festivals. Auto-refreshed quarterly. |

**Evidence snippet (Glastonbury feed, verbatim):**
```
BEGIN:VCALENDAR
PRODID:-//Smart Calendars AI//CalFeed//EN
REFRESH-INTERVAL;VALUE=DURATION:PT24H
BEGIN:VEVENT
DTSTART;VALUE=DATE:20260624
DTEND;VALUE=DATE:20260629
SUMMARY;LANGUAGE=en:Glastonbury 2026
LOCATION;LANGUAGE=en:Worthy Farm, Pilton, Somerset, UK
END:VEVENT
...
```

**Evidence snippet (Coachella feed — the accuracy problem, verbatim summaries):**
```
SUMMARY:Coachella Music Festival - Weekend 1 (April 9-11, 2027)
SUMMARY:Coachella Music Festival - Weekend 2 (April 16-18, 2027)
SUMMARY:Parking Pass: Cadillac Championship - Wednesday 2026   <-- hallucinated / wrong event
SUMMARY:Next Coachella Festival Dates – date TBA [CANCELLED]
```

Smart Calendars AI also offers per-artist feeds (Taylor Swift, Beyoncé, Bad Bunny, etc., auto-refreshed daily) and a Germany aggregate (111 events) — same accuracy caveat applies; out of scope for tentpole festivals.

---

## REJECTED / UNSUITABLE OPTIONS

- **Smart Calendars AI as source-of-record — REJECTED for accuracy.** Feeds are live and free, but verification surfaced hallucinated events, duplicates, wrong durations, and false cancellation tags. Fine as a *background signal*, unacceptable as the published feed for an accuracy-sensitive client. Also single-vendor risk (a startup app; feeds could disappear).
- **Songkick `.ics` feeds** — only export a *user's own* "going/interested" attendances (`songkick.com/users/USERNAME/calendars.ics`). No public festival-dates feed. Not fit for purpose.
- **Clashfinder** — offers `.ics` export per festival, but it is **set-level timetable data** (every artist/stage/time). Far too granular for tentpole entries; also community-maintained per event, high maintenance.
- **Bandsintown / Songkick APIs** — concert/tour data keyed to artists and venues, not clean "festival = one multi-day event" records. Would require heavy custom aggregation and dedup.
- **Official festival websites** — publish dates as HTML only; **no `.ics` subscription** found on any (Coachella, Glastonbury, Ultra, Tomorrowland, Lollapalooza, EDC, Reading & Leeds). They are the best *authoritative data source* for a custom calendar, just not a subscribable feed.
- **calendarlabs.com / generic "iCal calendar" sites** — holidays/observances only; no festival coverage.

---

## RECOMMENDED APPROACH — Custom Curated, Yearly Refresh

**Why:** Festival dates are announced 6–12 months ahead and change only once per year, so maintenance is genuinely low. A curated list avoids the AI-feed accuracy risk entirely and lets us pick exactly the tentpole set Pyros wants (one entry per festival, spanning its dates).

**Maintenance cadence:** one full refresh each January + one mid-year check (e.g. July) to capture newly announced next-year dates. ~1–2 hours per pass.

**Authoritative data sources to curate from (in priority order):**
1. **Each festival's official website** (dates are posted on the homepage/FAQ — most authoritative).
2. **Music Festival Wizard** (musicfestivalwizard.com) — reliable per-festival pages with confirmed dates; good aggregator for cross-checking.
3. **Billboard Music Industry Events Calendar** (billboard.com/pro) — industry-grade dated list.
4. Festival press (DJ Mag, Radio X, EDM.com, Beatportal) for date-announcement news.

### Suggested tentpole set + confirmed dates in the rolling window (Jul 2026 → Jul 2027)

> Note: Coachella, Glastonbury, Tomorrowland Belgium, EDC LV and Ultra's 2026 editions all occur *before* 2026-07-21 and fall outside the forward window. Listed below are the editions that land inside the rolling 12 months.

**Remaining 2026:**
- **Lollapalooza** (Chicago) — Jul 30 – Aug 2, 2026 *(confirmed, official)*
- **Reading & Leeds** (UK) — Aug 27–30, 2026 *(confirmed)*
- **Austin City Limits** (Austin) — Oct 2–4 & Oct 9–11, 2026 *(confirmed, two weekends)*

**2027:**
- **Ultra Music Festival** (Miami) — Mar 26–28, 2027 *(confirmed on official site)*
- **Tomorrowland Winter** (Alpe d'Huez, France) — Mar 20–27, 2027 *(reported)*
- **Coachella** (Indio) — Apr 9–11 & Apr 16–18, 2027 *(confirmed, two weekends)*
- **EDC Las Vegas** (new "Dusk Till Dawn" format) — Dusk May 14–16, Dawn May 21–23, 2027 *(reported)*
- **Glastonbury** (Worthy Farm) — Jun 23–27, 2027 *(reported; not yet confirmed on official site)*
- **Tomorrowland Belgium** — Jul 17–19 & Jul 24–26, 2027 *(reported)*
- **Tomorrowland Las Vegas** (debut) — 2027, dates TBA *(announced, watch for confirmation)*

Additional candidates to consider for the tentpole set: Stagecoach, Bonnaroo, Governors Ball, Outside Lands, Primavera Sound, Rock in Rio, Rolling Loud, Sziget, Wireless, Parklife, Creamfields, Electric Forest.

---

## Verification log

- Fetched `smartcalendars.ai/cal/...glastonbury.ics` → HTTP 200, valid VCALENDAR, 2 VEVENTs. ✔
- Fetched Coachella / EDC / US-aggregate / Download / Bonnaroo / ACL feed URLs → all HTTP 200, valid VCALENDAR. ✔
- US aggregate = 61 VEVENTs; confirmed duplicates (Coachella 3×) and minor-festival noise. ✔
- Coachella feed contains hallucinated "Cadillac Championship parking pass" event. ✔ (accuracy disqualifier)
- Confirmed via WebSearch: no official `.ics` on any major festival site; Songkick `.ics` is user-attendance only; Clashfinder `.ics` is set-level. ✔

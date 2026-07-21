# Technology & Social Media — Tentpole Calendar Feed Research

**Category:** Technology & Social Media
**Use case:** Pyros content-planning "tentpole" calendar (broad marquee events, one entry per event)
**Research date:** 2026-07-21
**Target window:** 2026-07-21 → ~2027-07 (rolling 12 months)
**Bottom line:** No single official auto-updating .ics feed covers these tentpoles across a full 12-month horizon. The best zero-maintenance live feed that exists is **Techmeme's public events .ics** (verified live), but it is a near-term rolling window (~4–5 months out) and contains noise (earnings, minor dev cons). **Recommended approach = a custom curated, yearly-refreshed calendar** for the 12-month tentpole horizon, optionally *supplemented* by the Techmeme feed for near-term exact keynote dates.

---

## VERIFIED OPTIONS (feed actually fetched and confirmed live)

### 1. Techmeme Events — public .ics feed  ✅ VERIFIED LIVE
- **Provider:** Techmeme (established, authoritative tech-news aggregator)
- **Full feed URL:** `https://techmeme.com/events.ics`
- **Curated ("newsy") subset URL:** `https://techmeme.com/newsy_events.ics`
- **Official?** Not official to any single event, but an authoritative curated aggregator. Techmeme publicly publishes these feeds and explicitly invites calendar subscription (announced 2016).
- **Price:** Free
- **Update cadence:** Auto-updating, continuously maintained by Techmeme staff. Zero maintenance for us.
- **Maintenance burden:** None (subscribe once).
- **Reliability:** High for what it covers; long-running, stable.
- **Legal/ToS:** Publicly offered for subscription; attribution string ("From Techmeme's event calendar") is embedded in each event's DESCRIPTION. Subscribing is within intended use.

**Verification evidence (fetched 2026-07-21):**
- `https://techmeme.com/events.ics` → **HTTP 200**, 129,770 bytes, **117 VEVENTs**
- `https://techmeme.com/newsy_events.ics` → **HTTP 200**, 29,882 bytes, **26 VEVENTs**
- Header confirms valid iCalendar:
  ```
  BEGIN:VCALENDAR
  VERSION:2.0
  PRODID:-//techmeme.com//events//full
  METHOD:PUBLISH
  X-WR-CALNAME:Techmeme events
  BEGIN:VEVENT
  ...
  SUMMARY:SIGGRAPH
  ```
- Marquee tentpoles confirmed present in the feed today: **Samsung Galaxy Unpacked (2026-07-22)**, **Made By Google / Pixel event (2026-08-12)**, **gamescom (2026-08-26)**, **IFA (2026-09-04)**, **Qualcomm Snapdragon Summit (2026-09-22)**, **Meta Connect (2026-09-23)**, **OpenAI DevDay (2026-09-29)**, **MWC Las Vegas (2026-10-14)**, **TwitchCon (2026-11-12)**, **Microsoft Ignite (2026-11-16)**.

**Limitations (important for our use case):**
1. **Horizon is short.** Current feed spans only **2026-07-19 → 2026-11-26** (~4–5 months). Events further out (CES Jan 2027, MWC Barcelona Mar 2027, WWDC/Google I/O/Computex 2027) are **NOT yet in the feed** — Techmeme adds them as they enter the near-term window. So it **cannot** fill a fixed 12-month planning calendar on its own.
2. **Granularity is finer than "marquee only."** The full feed includes quarterly earnings dates, security cons (Black Hat, DEF CON), and many mid-tier dev conferences — not "one entry per marquee event." The "newsy" subset is smaller but is still dominated by **Earnings** entries (noise for a promo calendar).
3. **Naming/curation is Techmeme's, not ours** — we can't rename or trim entries in a subscribed feed.

**Verdict:** Great as a *live supplementary* feed for catching exact keynote dates in the coming ~4 months with zero effort. Not sufficient as the primary 12-month tentpole source.

---

## REJECTED / NOT SUITABLE

- **Individual event organizers (CES/CTA, MWC/GSMA, Apple, Google, Samsung, Meta, gamescom, IFA):** Searched; **none publish a public auto-updating .ics feed of their marquee/keynote date** for external subscription. They publish dates on their websites (and some offer per-session "add to calendar" .ics buttons behind registration, which are not usable as a standing public feed). → No verifiable standing feed to recommend.
- **Fastly developer-events .ics (`developer.fastly.com/downloads/events.ics`):** Exists but is Fastly-specific developer events — irrelevant to consumer-tech tentpoles. Not fetched/recommended.
- **Blog "2026 tech calendar" listicles (techloy, vfairs, bitcot, countdown-timer, etc.):** Useful as cross-reference data sources, but they are HTML articles, **not .ics feeds**, and are not authoritative for exact dates.

## UNVERIFIED (mentioned in search, not confirmed live — do NOT rely on)
- GitHub tooling like **GitEvents ICS** / **all-in-one-event-calendar**: these are *generators* you'd have to run and host yourself, not a ready public tentpole feed. Not fetched. Effectively "build your own," which collapses into the custom-calendar recommendation below.

---

## VERIFIED TENTPOLE DATES (for building/refreshing a custom calendar)

Dates below were confirmed via official event sites and/or Apple Newsroom during this research. Predicted 2027 dev-event dates are marked; they recur at predictable times and should be confirmed at yearly refresh.

| Event | Date | Status / Source |
|---|---|---|
| Samsung Galaxy Unpacked (Fold/Flip) | **2026-07-22** (London) | Confirmed (Samsung / press) |
| gamescom (Cologne) + Opening Night Live | **Aug 26–30, 2026** (ONL Aug 25) | Confirmed (gamescom.global) |
| Apple September event (iPhone 18) | **~Sept 8–9, 2026** | *Rumored/predicted* (Apple not yet announced) |
| IFA Berlin | **Sept 4–8, 2026** | Confirmed (visitBerlin / IFA) |
| Qualcomm Snapdragon Summit | **~Sept 22, 2026** | Per Techmeme feed |
| Meta Connect | **~Sept 23, 2026** | Per Techmeme feed |
| MWC Las Vegas | **Oct 14, 2026** | Per Techmeme feed |
| Microsoft Ignite | **~Nov 16, 2026** | Per Techmeme feed |
| **CES 2027** (Las Vegas) | **Jan 6–9, 2027** | Confirmed official (CES / CTA) — recurs early Jan |
| Samsung Galaxy Unpacked (Galaxy S26) | **~late Jan / early Feb 2027** | *Predicted* (annual pattern) |
| **MWC Barcelona 2027** | **March 1–4, 2027** | Confirmed official (mwcbarcelona.com) — recurs late Feb/early Mar |
| Google I/O 2027 | **~May 2027** | *Predicted* (annual pattern; I/O 2026 was May) |
| WWDC 2027 (Apple) | **~week of June 7, 2027** | *Predicted* (WWDC 2026 was June 8–12) |
| Computex 2027 (Taipei) | **~early June 2027** | *Predicted* (Computex 2026 was June 2–5) |

**Authoritative data sources for the yearly refresh:**
- CES: ces.tech / cta.tech
- MWC Barcelona + MWC Las Vegas: mwcbarcelona.com / mwclasvegas.com (GSMA)
- Apple (WWDC + Sept event): apple.com/newsroom
- Google I/O: io.google
- Samsung Unpacked: news.samsung.com
- Meta Connect: meta.com / developers.meta.com
- gamescom: gamescom.global ; IFA: ifa-berlin.com ; Computex: computextaipei.com.tw
- **Live cross-check:** Techmeme events feed (above) to catch exact keynote dates as they're announced.

---

## FINAL RECOMMENDATION

**Primary: Build a custom curated "Tech & Social Media Tentpole" calendar, refreshed yearly.**
- ~12–14 marquee entries per year, one per event, using the verified dates + official sources above.
- Most anchor events recur at predictable times (CES early Jan, MWC Barcelona late Feb/early Mar, Google I/O ~May, WWDC/Computex ~June, Samsung Unpacked Jul + Jan/Feb, gamescom late Aug, Apple iPhone + IFA + Meta Connect Sept), so a once-a-year refresh (plus quick date confirmation as each approaches) is low effort and gives the full 12-month horizon Pyros needs.
- Keep it as our own .ics we control (naming, trimming, promo notes) — no dependency on a third party's granularity.

**Supplement (optional, zero-maintenance): subscribe to `https://techmeme.com/events.ics`.**
- Use it as a live radar to auto-catch exact keynote dates and newly announced events in the coming ~4–5 months. It is verified live and auto-updates. Treat it as an input to confirm/adjust the curated calendar, not as the client-facing calendar itself (too much earnings/dev-con noise, and horizon too short to stand alone).

**Do NOT** rely on any single official event .ics feed — none exists for these tentpoles that we could verify.

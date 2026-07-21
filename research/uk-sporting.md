# UK Sporting Events — Calendar Feed Research

**Category:** UK Sporting Events (tentpole / season-level)
**Researched:** 2026-07-21
**Target window:** 2026-07-21 → rolling ~12 months
**Granularity goal:** Broad tentpoles (Wimbledon, Six Nations, Grand National, The Open, The Ashes, London Marathon, FA Cup Final, British GP, etc.) — NOT every individual fixture.

---

## TL;DR

There is **no official, single, auto-updating .ics feed** for "UK sporting tentpoles." Official governing bodies (LTA/Wimbledon, RFU, R&A, ECB, Jockey Club, London Marathon) do **not** publish a clean tentpole iCalendar feed.

The best live, free, auto-updating aggregator found and verified is **sporting-events.org**, which does publish valid `.ics` feeds with genuine tentpole-level titles. However it is a **third-party site of unknown provenance**, its feeds are organised **by sport (global), not by country**, and it has **visible coverage gaps/lag** (e.g. Wimbledon 2027 currently absent; no Royal Ascot, Epsom Derby, Boat Race, or a distinct FA Cup Final entry). For a client who cares deeply about accuracy, it is safe as a **scaffold/cross-check**, not as the sole source of truth.

**Recommendation: build a custom curated, yearly-refreshed UK tentpole calendar (~30–40 events), seeded and cross-checked against the verified sporting-events.org feeds + authoritative event sources.** Details at the bottom.

---

## VERIFIED options (fetched live, confirmed valid iCalendar)

### 1. sporting-events.org — per-sport & master `.ics` feeds  ⭐ best live candidate

- **Provider:** sporting-events.org ("Sports Calendar Subscriptions")
- **Official?** No — independent third-party aggregator.
- **Price:** Free. No signup, no email.
- **Format:** Valid iCalendar. `PRODID:-//sporting-events.org//SE Feeds 1.0//EN`, `METHOD:PUBLISH`, `REFRESH-INTERVAL / X-PUBLISHED-TTL: PT12H`.
- **Update cadence:** Server refreshes continuously; feed advertises 12h TTL. Most calendar apps re-poll every 12–24h. **Zero maintenance once subscribed.**
- **Granularity:** Mostly tentpole/tournament/festival level (good) — but some series are split per-round/per-match (Six Nations → Round 1 / Round 3 / Super Saturday; The Ashes → 5 Tests; darts → multiple ranking events).
- **Scope problem:** Feeds are per-SPORT and **global**. e.g. `golf.ics` includes US PGA + Ryder/Presidents Cup; `all.ics` includes every F1 GP worldwide, US college football, Berlin/Chicago/NYC marathons. **UK events must be filtered out of the noise.**

**Verification evidence (HTTP 200, `Content-Type: text/calendar`, all contain `BEGIN:VCALENDAR`):**

| Feed | URL | HTTP | VEVENTs | Notes |
|---|---|---|---|---|
| Master (all sports) | `https://sporting-events.org/feeds/all.ics` | 200 | 1000 | Global, very noisy |
| Six Nations | `https://sporting-events.org/feeds/six-nations.ics` | 200 | 3 | 2027 rounds only |
| Horse Racing | `https://sporting-events.org/feeds/horse-racing.ics` | 200 | 18 | Incl. Grand National 2027, Cheltenham 2027, Goodwood, Ebor, St Leger, King George VI Chase |
| Golf | `https://sporting-events.org/feeds/golf.ics` | 200 | 28 | Incl. The Open, AIG Women's Open, The Masters 2027, Ryder Cup 2027 |
| Cricket | `https://sporting-events.org/feeds/cricket.ics` | 200 | 15 | Incl. The Hundred, England Tests, full Ashes 2026-27 |
| Tennis | `https://sporting-events.org/feeds/tennis.ics` | 200 | (valid) | — |
| Wimbledon | `https://sporting-events.org/feeds/wimbledon.ics` | 200 | **0** | **Empty** — 2026 just finished, 2027 not yet added (coverage lag) |
| Premier League | `https://sporting-events.org/feeds/premier-league.ics` | 200 | ~91 | **Too granular** — every fixture |

Sample raw header (`wimbledon.ics`):
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//sporting-events.org//SE Feeds 1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Wimbledon Calendar – Sporting Events
REFRESH-INTERVAL;VALUE=DURATION:PT12H
END:VCALENDAR
```

Sample events actually present (tentpole-quality titles + dates):
```
20260716  The Open Championship            Southport, United Kingdom
20260721  The Hundred
20261017  QIPCO British Champions Day
20261210  PDC World Darts Championship
20270313  Six Nations 2027: Super Saturday
20270410  Grand National 2027
20270425  London Marathon 2027
20261126  The Ashes (1st Test)             Brisbane, Australia
```

**Subscription helper URLs (same feed, wrapped):** Google Calendar `https://calendar.google.com/calendar/r?cid=webcal%3A%2F%2Fsporting-events.org%2Ffeeds%2F<slug>.ics` · Apple `webcal://sporting-events.org/feeds/<slug>.ics` · Outlook `https://outlook.live.com/calendar/0/addfromweb?url=https%3A%2F%2Fsporting-events.org%2Ffeeds%2F<slug>.ics`.

**Concerns / risks:**
- **Provenance/longevity unknown** — no named owner; a hobbyist aggregator could go offline without notice.
- **Accuracy not guaranteed** — no SLA. Observed gaps: Wimbledon 2027 absent, no Royal Ascot, Epsom Derby, The Boat Race, Henley, Snooker World Championship, or a distinct "FA Cup Final" (only "FA Cup Third Round"). Several are absent simply because the 2026 running has passed and 2027 isn't loaded yet — i.e. there is refresh lag near the rolling edge.
- **Not UK-scoped** — needs filtering.
- **ToS:** Personal subscription explicitly invited ("no catch"). Re-publishing/redistributing the data inside a commercial product is not addressed by the site and should not be assumed permitted — treat it as a reference input, not content to rebroadcast.

---

## REJECTED / not suitable

| Provider | Why rejected |
|---|---|
| **Premier League / ecal.com, fixtur.es, matchesio, fixturedownload.com, calendarteams.com** | All are **per-fixture** football feeds (380 matches). Far too granular for a tentpole calendar. Could at most inform a single "Premier League season start" entry. |
| **Sky Sports `/calendars`** | Feeds exist but are generated per team/competition via an on-page "add to calendar" widget (no static tentpole URL); page redirected/blocked on fetch — **could not retrieve a verifiable feed URL**. Also fixture-level. |
| **awarenessdays.com/sporting-calendar** | Returned **HTTP 403** to automated fetch. Web-page calendar, no confirmed `.ics` feed. UNVERIFIED. |
| **Official event sites (wimbledon.com, RFU, R&A, ECB, thejockeyclub.co.uk, londonmarathonevents.co.uk)** | No public tentpole `.ics` feed found for any of them. They publish dates on web pages only. |
| **calendarlabs.com / calendar2026.co.uk / localpage.uk / VisitBritain / sportstourismnews** | Human-readable listicles/date pages. Good as **authoritative date cross-checks**, but **not** machine feeds. |

*(No URL in this document was guessed — every `.ics` URL under "Verified" was fetched and returned HTTP 200 with `text/calendar` content beginning `BEGIN:VCALENDAR`.)*

---

## FINAL RECOMMENDATION

**Build a custom curated, yearly-refreshed UK tentpole calendar (~30–40 events/year).**

**Why (not the auto feed):**
1. **Accuracy** — client-critical. A curated list we control has no third-party gaps, no global noise, and no dependence on an anonymous site staying online and correct.
2. **Low burden anyway** — tentpole dates are announced 6–18 months ahead and rarely move. This is a ~1–2 hour refresh **once a year**, not ongoing maintenance. It genuinely satisfies the "little-to-no maintenance" priority for this category.
3. **Correct granularity & scope** — we pick exactly the UK marquee moments at the level Pyros wants (one "Wimbledon 2026" block, one "The Open", one "Grand National"), UK-only.

**How:**
- Maintain a small curated list → generate `.ics` yearly with the project's tooling. Seed the FIRST build directly from the **verified sporting-events.org feeds** (they already contain clean titles/dates for Six Nations, The Open, The Hundred, Ashes, Cheltenham, Grand National, London Marathon, British Champions Day, PDC Darts, etc.).
- **Cross-check every date** against the authoritative source below before publishing.
- Optionally also **subscribe to `all.ics` as a live secondary cross-check / early-warning** for date changes — but do not treat it as the primary.

**Authoritative data sources for the yearly refresh (cross-check dates here):**
- **VisitBritain — "Britain's sporting highlights"** annual roundup (curated tentpole list). https://www.visitbritain.org
- Each event's **official site**: wimbledon.com · sixnationsrugby.com · aintree.thejockeyclub.co.uk (Grand National) · theopen.com / randa.org · ecb.co.uk (The Ashes / The Hundred) · tcslondonmarathon.com · thefa.com (FA Cup Final) · silverstone.co.uk / formula1.com (British GP) · ascot.com (Royal Ascot) · theboatrace.org.

**Core UK tentpole events to include (rolling 12-month, this window):**
The Open Championship · The Hundred · England home Test series · QIPCO British Champions Day · PDC World Darts Championship · The Ashes (2026-27, away in Australia but huge UK audience) · Six Nations 2027 · Cheltenham Festival 2027 · Grand National 2027 (Aintree) · London Marathon 2027 · The Masters / Ryder Cup 2027 · plus manually add (missing from the feed, add from official sites): **Wimbledon**, **Royal Ascot**, **Epsom Derby**, **The Boat Race**, **FA Cup Final**, **British Grand Prix (Silverstone)**, **Snooker World Championship**, **Great North Run**.

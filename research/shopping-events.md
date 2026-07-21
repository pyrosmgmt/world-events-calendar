# Shopping Events — Calendar Feed Research

**Category:** Shopping Events (retail/e-commerce tentpoles)
**Purpose:** Content-planning tentpole calendar for the Pyros team (OnlyFans management) — prime promotion moments.
**Research date:** 2026-07-21
**Target window:** now → rolling ~12 months (through ~2027-07)

---

## TL;DR / Recommendation

**There is no reliable, official, auto-updating `.ics` feed for retail shopping tentpoles** (Black Friday, Cyber Monday, Prime Day, Singles' Day, etc.). These are commercial/marketing events, not civic holidays, so no authoritative body publishes them as a calendar feed. Every "e-commerce marketing calendar" found online is a **blog article or downloadable PDF/spreadsheet**, not a subscribable feed.

**Recommended approach: build a custom curated `.ics`, refreshed yearly.** Almost all of these dates are either fixed (Nov 11, Dec 26, Feb 14) or follow a deterministic weekday rule (Black Friday = day after US Thanksgiving), so a hand-built recurring calendar is highly reliable and near-zero maintenance. The one genuine exception is **Amazon Prime Day**, which is unpredictable and must be confirmed from Amazon's official announcement each year (see below).

---

## Verification log (feeds actually fetched)

| Provider | Feed URL | HTTP | Valid iCal? | Contains shopping events? | Verdict |
|---|---|---|---|---|---|
| **Office Holidays — USA** | `https://www.officeholidays.com/ics/usa` | 200 | Yes — `BEGIN:VCALENDAR`, 42 `VEVENT`, `REFRESH-INTERVAL PT48H` | **No** — public holidays only | Live & reliable, but wrong content. Usable only as a *date anchor* for Thanksgiving / Memorial Day / Labor Day. |
| CalendarLabs — Holidays index | `https://www.calendarlabs.com/ical-calendar/holidays/` | 200 | Index page (per-country `.ics` behind it) | No shopping category exists | Public-holidays only; same limitation. |

**Evidence snippet — Office Holidays USA feed header:**
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Office Holidays Ltd.//EN
X-WR-CALNAME:USA Holidays
REFRESH-INTERVAL;VALUE=DURATION:PT48H
```
Its 42 events include "Thanksgiving" and "Day after Thanksgiving (Regional Holiday)" but **no** "Black Friday", "Cyber Monday", "Prime Day", "Singles' Day", or "Boxing Day". Confirmed by scanning every `SUMMARY` line — zero shopping matches.

**Feeds NOT found / UNVERIFIED:** No `.ics` feed for a dedicated shopping/e-commerce calendar was located on icalshare, awarenessdays.com (offers an iCal feed but no public direct shopping URL was retrievable), Shopify, Omnisend, Printful, or OptinMonster — all publish articles/PDFs only. Nothing here is recommended because nothing could be fetched and verified.

---

## The date RULES (so we can generate any year reliably)

All US "Monday/Thursday" holidays follow fixed weekday-of-month rules. Verified computed dates for the target window:

| Event | Rule | 2026 | Next (2027) | Region |
|---|---|---|---|---|
| **Valentine's Day** | Fixed **Feb 14** | — | 2027-02-14 | Global |
| **US Presidents' Day sales** | **3rd Monday of February** | — | 2027-02-15 | US |
| **US Memorial Day sales** | **Last Monday of May** | — | 2027-05-31 | US |
| **Amazon Prime Day** | *No rule — Amazon announces.* 2026 = **Jun 23–26** (moved to June); historically 2nd week of July. | 2026-06-23→26 (passed) | TBA — confirm from Amazon | Global (Prime markets) |
| **Back-to-School peak** | Season, not a day. US peak ~ **late Jul–early Sep**; anchor early August | ~Aug 2026 | ~Aug 2027 | US |
| **US Labor Day sales** | **1st Monday of September** | 2026-09-07 | 2027-09-06 | US |
| **Singles' Day (11.11)** | Fixed **Nov 11** | 2026-11-11 | 2027-11-11 | Global (China-origin) |
| **Thanksgiving (US)** | **4th Thursday of November** | 2026-11-26 | 2027-11-25 | US |
| **Black Friday** | **Day after US Thanksgiving** (4th Friday of Nov) | 2026-11-27 | 2027-11-26 | Global |
| **Small Business Saturday** | **Saturday after Thanksgiving** | 2026-11-28 | 2027-11-27 | US |
| **Cyber Monday** | **Monday after Thanksgiving** | 2026-11-30 | 2027-11-29 | Global |
| **Green Monday** | **2nd Monday of December** | 2026-12-14 | 2027-12-13 | US e-comm |
| **Boxing Day** | Fixed **Dec 26** | 2026-12-26 | 2027-12-26 | UK / CA / AU |
| **New Year sales** | Fixed **Jan 1** (runs late-Dec→early-Jan) | — | 2027-01-01 | Global |

> Note on "Cyber 5": Black Friday → Cyber Monday form a contiguous 5-day block (Thanksgiving through Cyber Monday). For 2026 that's **Nov 26–30**.

### Caution / accuracy notes
- **Do not trust AI/blog date summaries.** During research, a summary claimed Black Friday 2026 = "Nov 28" and Cyber Monday = "Dec 1" — those are **2025** dates. The verified 2026 dates (computed from the rule) are **Nov 27** and **Nov 30**. Always generate from the weekday rule.
- **Prime Day is the maintenance risk.** It has no fixed rule and Amazon moves it (June in 2021 and 2026, July most other years). Confirm each year from the official Amazon Newsroom post (`aboutamazon.com/news` — "When is Amazon Prime Day"). Amazon usually also runs a **fall "Prime Big Deal Days"** event in October — confirm separately.

---

## Candidate providers (detail)

**Office Holidays (`officeholidays.com/ics/usa`)** — Official? No (third party). Price: free. Cadence: auto-refresh every 48h. Maintenance: zero. Reliability: high (well-established). ToS: personal/business subscription OK; redistribution not permitted. Granularity: **does not fit** — civic holidays only, no shopping events. *Use only as an anchor feed for Thanksgiving/Memorial/Labor Day if desired.*

**CalendarLabs** — Same profile as above: reliable public-holiday feeds, no shopping category. Does not fit.

**awarenessdays.com** — Advertises an iCal feed for 1,900+ "awareness days," may include some retail observances, but no public direct feed URL was retrievable to verify, and content skews to awareness/novelty days rather than commercial sale tentpoles. **UNVERIFIED — not recommended.**

**E-commerce marketing calendars (Shopify, Omnisend, Printful, OptinMonster, etc.)** — Good authoritative *reference sources for the date list*, but delivered as articles/PDF/spreadsheet, **not** `.ics`. Use them to sanity-check the curated calendar, not to subscribe.

---

## Final RECOMMENDATION

1. **Build one custom curated `.ics`** for Shopping Events, generated by a small script from the weekday rules above (fixed dates + Nth-weekday helpers). This is deterministic, correct, and refreshes with a **once-a-year** regeneration.
2. **Confirm Prime Day (and fall Prime Big Deal Days) manually each year** from Amazon's official announcement — the only non-rule-based item. Add as an all-day multi-day block once announced (typically announced 3–4 weeks prior).
3. **(Optional) Also subscribe to the Office Holidays USA feed** purely as a live cross-check anchor for Thanksgiving/Memorial Day/Labor Day dates, since Black Friday etc. derive from Thanksgiving.
4. Tag each event with its **region** (US vs UK/CA/AU vs Global) so promo planning targets the right audience — Boxing Day is UK/CA/AU, several sale weekends are US-only.

**Authoritative sources for the dates:** US federal holiday rules (fixed by statute → Thanksgiving/Memorial/Labor/Presidents' Day) for the rule-based events; Amazon Newsroom (`aboutamazon.com`) for Prime Day; fixed-calendar dates (Nov 11, Dec 26, Feb 14, Jan 1) need no source.

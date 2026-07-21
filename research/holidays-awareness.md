# Holidays & Awareness — Feed Research

**Category:** Holidays & Awareness (tentpole content-planning calendar)
**Primary regions:** UK + US (major global secondary)
**Target window:** rolling ~12 months from 2026-07-21
**Research date:** 2026-07-21
**Priority:** correct + low/zero maintenance feeds.

---

## TL;DR Recommendation

1. **UK public holidays + major cultural days** → Google's official "Holidays in United Kingdom" `.ics` (auto-updating, zero maintenance). VERIFIED LIVE.
2. **US public holidays + major cultural days** → Google's official "Holidays in United States" `.ics` (auto-updating, zero maintenance). VERIFIED LIVE.
3. **Authoritative UK bank-holiday truth source (for validation / rebuild)** → `https://www.gov.uk/bank-holidays.json`. VERIFIED LIVE.
4. **Fallback / multi-country programmatic source** → Nager.Date API (build our own feed, yearly refresh). VERIFIED LIVE.
5. **Awareness/fun social days NOT in the Google feeds** (Int'l Women's Day, Pride, quirky viral days) → **curate a vetted internal shortlist**; do not trust random "National X Day" registries.

---

## 1. Google Official Public Holiday Calendars — RECOMMENDED (zero maintenance)

Google publishes read-only, auto-updating holiday calendars per country. They include statutory public/bank holidays **and** major cultural observances useful for content.

### UK feed — VERIFIED
- **Provider:** Google Inc. (official Google Calendar holiday calendar)
- **Subscription URL (.ics):**
  `https://calendar.google.com/calendar/ical/en.uk%23holiday%40group.v.calendar.google.com/public/basic.ics`
  (raw calendar ID: `en.uk#holiday@group.v.calendar.google.com`)
- **Official?** Yes (Google-maintained)
- **Price:** Free
- **Update cadence:** Continuous / auto-updating (subscribe once, never touch again)
- **Maintenance burden:** None
- **Verification:** `HTTP 200`, 95,699 bytes, `Content` valid iCalendar.
  - Header: `BEGIN:VCALENDAR` / `PRODID:-//Google Inc//Google Calendar 70.9054//EN` / `X-WR-CALNAME:Holidays in United Kingdom` / `X-WR-CALDESC:Holidays and Observances in United Kingdom`
  - **244 VEVENT** entries; coverage span **2021-01-01 → 2031-12-31** (well beyond our 12-month window).
  - Sample SUMMARY values: New Year's Day, Good Friday, Christmas Day, Boxing Day, Substitute Bank Holiday for Christmas Day, **Valentine's Day, Halloween, Mother's Day, Father's Day, New Year's Eve, Christmas Eve, Carnival / Shrove Tuesday / Pancake Day**.

### US feed — VERIFIED
- **Provider:** Google Inc.
- **Subscription URL (.ics):**
  `https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics`
  (raw calendar ID: `en.usa#holiday@group.v.calendar.google.com`)
- **Official?** Yes
- **Price:** Free
- **Update cadence:** Continuous / auto-updating
- **Maintenance burden:** None
- **Verification:** `HTTP 200`, 120,685 bytes, valid iCalendar.
  - Header: `X-WR-CALNAME:Holidays in United States` / `X-WR-CALDESC:Holidays and Observances in United States`
  - **317 VEVENT** entries; coverage span through **2031-12-31**.
  - Sample SUMMARY values: Martin Luther King Jr. Day, Veterans Day, **Valentine's Day, Halloween, Mother's Day, Father's Day, Cinco de Mayo, Black Friday, Christmas Eve, Tax Day, Flag Day, Daylight Saving Time starts**.

### Notes on the Google feeds
- The `%23` and `%40` in the URL are just URL-encoded `#` and `@` — required for the feed to resolve. Use the encoded form in software; the decoded ID works in the Google Calendar "Add by URL" box.
- Language/scope can be varied via the `en.<locale>` prefix (e.g. `en.usa`, `en.uk`). These "Holidays and Observances" variants include cultural days; there are stricter "public holidays only" variants but the observances version is what we want for content planning.
- **ToS / legal:** These are Google's public subscribe-able calendars intended for exactly this use (subscription in calendar apps). Low risk for internal planning. If we ever *redistribute* the data commercially, prefer the government/Nager sources below as the licensed backbone.
- **Reliability:** Very high — Google-hosted, globally cached, auto-corrects future dates (e.g. moveable feasts, substitute bank holidays).

---

## 2. gov.uk Bank Holidays JSON — RECOMMENDED as authoritative UK source

The definitive UK government source. Best used as the **truth reference** to validate the Google feed, or to build our own UK feed if we want full control.

- **Provider:** UK Government (GDS / gov.uk)
- **Exact URL:** `https://www.gov.uk/bank-holidays.json`
- **Format:** JSON (NOT .ics). `Content-Type: application/json; charset=utf-8`
- **Official?** Yes — the canonical government endpoint
- **Price:** Free, no auth/API key
- **Update cadence:** Updated by gov.uk when holidays are set/changed (e.g. one-off royal holidays). Effectively self-maintaining; we'd re-pull periodically.
- **Maintenance burden:** Low (if we build a feed from it, a yearly/scheduled refresh script; the JSON itself is maintained by the government).
- **Verification:** `HTTP 200`, 22,207 bytes, valid JSON.
  - Structure: three divisions — `england-and-wales`, `scotland`, `northern-ireland` — each with an `events` array of `{title, date (YYYY-MM-DD), notes, bunting}`.
  - Sample: `{"title":"New Year's Day","date":"2019-01-01","notes":"","bunting":true}` … includes Good Friday, Easter Monday, Early May / Spring / Summer bank holidays, Christmas Day.
- **Caveat:** Statutory **bank holidays only** — no cultural/awareness days (no Valentine's, Halloween, etc.). Would need our own build step to turn JSON → .ics.

---

## 3. Nager.Date API — Fallback / multi-country programmatic source

Good if we want to generate our own feed or add more countries beyond UK/US with one integration.

- **Provider:** Nager.Date (open-source public holiday API)
- **Exact URLs (verified):**
  - `https://date.nager.at/api/v3/PublicHolidays/2026/GB`
  - `https://date.nager.at/api/v3/PublicHolidays/2026/US`
  - Pattern: `https://date.nager.at/api/v3/PublicHolidays/{year}/{ISO2countrycode}`
- **Format:** JSON (build .ics from it)
- **Official?** No (community/open project, but widely used and accurate for statutory holidays)
- **Price:** Free, no key
- **Update cadence:** We call per-year → **yearly refresh** required (year is in the path).
- **Maintenance burden:** Medium — needs a small script + annual re-run; we own the .ics generation.
- **Verification:** GB `HTTP 200` (2,646 bytes), US `HTTP 200` (3,700 bytes), valid JSON arrays.
  - GB sample: `{"date":"2026-01-01","localName":"New Year's Day","countryCode":"GB","counties":["GB-ENG","GB-NIR","GB-SCT","GB-WLS"],"types":["Public"]}`; includes Scotland-only "2 January" and "Saint Patrick's Day" with per-county scoping.
  - US sample: `{"date":"2026-01-01","localName":"New Year's Day","countryCode":"US","global":true,"types":["Public","Bank"]}`.
- **Caveat:** Statutory holidays only — no awareness/fun days. Per-county granularity is a plus for UK devolved nations.

**Verdict on 2 & 3:** Keep as backups / validation. For a zero-maintenance content calendar, the Google feeds (Section 1) already deliver holidays **and** the big cultural tentpoles in one subscribe-once .ics, so building from JSON is unnecessary unless we need custom control or many countries.

---

## 4. Awareness / Fun Social-Media Days — CURATE, don't auto-feed

### What the Google feeds already give us (no extra work)
Confirmed present in the UK/US Google feeds within our window: Valentine's Day, Halloween, Mother's Day, Father's Day, New Year's Eve, Christmas Eve, Pancake Day / Shrove Tuesday, Cinco de Mayo, Black Friday, Tax Day, Flag Day, Daylight Saving changes.

### What is MISSING and needs curation
The Google feeds contain ~29 unique observance types — they do **NOT** include:
- **International Women's Day** (Mar 8)
- **Pride Month** / Pride events (June)
- Most "**National ___ Day**" viral/quirky days (e.g. National Cat Day, National Boyfriend Day, etc.)
- Global awareness days/weeks/months generally

### Why not just subscribe to a "national days" feed
Many "National X Day" claims are **marketing-generated and unreliable** — competing registries (e.g. National Day Calendar, days-of-the-year sites) list conflicting dates, and some days are invented for promotion. Auto-ingesting these risks putting wrong/duplicate/junk dates into a client-facing plan. The client cares about accuracy, so an unvetted feed is a liability.

### Recommended approach: a small vetted internal shortlist
Maintain a **hand-curated list (~30-60 entries/year)** of awareness/fun days that are (a) genuinely relevant to an OnlyFans-management agency's content and (b) date-verified. Source candidates from, but manually confirm:
- **UN international days** (authoritative, fixed) — `un.org/en/observances` — for Int'l Women's Day, etc.
- **National Day Calendar** (`nationaldaycalendar.com`) and **Days of the Year** (`daysoftheyear.com`) — use only as *candidate* lists; cross-check each date before adding. Flag anything that only appears on one marketing site.
- Pride: use fixed anchors (Pride Month = June; NYC/London Pride dates vary yearly — verify annually).

Store this as a simple internal spreadsheet/CSV → generate a supplementary `.ics` we control. **Maintenance: ~1 short review per year** to confirm moveable/annual dates. This is the only piece needing human upkeep; keep it small and vetted rather than large and noisy.

---

## Final Recommendation

| Need | Source | URL | Maint. |
|---|---|---|---|
| **UK holidays + big cultural days** | Google official (VERIFIED) | `https://calendar.google.com/calendar/ical/en.uk%23holiday%40group.v.calendar.google.com/public/basic.ics` | **Zero** |
| **US holidays + big cultural days** | Google official (VERIFIED) | `https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics` | **Zero** |
| UK statutory truth source / validation | gov.uk (VERIFIED) | `https://www.gov.uk/bank-holidays.json` | Low |
| Multi-country / build-your-own fallback | Nager.Date (VERIFIED) | `https://date.nager.at/api/v3/PublicHolidays/{year}/{GB\|US}` | Yearly |
| Awareness/fun days (Women's Day, Pride, quirky) | **Curated internal shortlist** (UN + cross-checked) | n/a (build our own small .ics) | ~1×/yr review |

**Bottom line:** Subscribe to the two Google `.ics` feeds for a zero-maintenance backbone covering UK + US public holidays and the major cultural tentpoles through 2031. Keep gov.uk JSON as the authoritative UK cross-check and Nager.Date as a programmatic fallback. Layer a small, hand-vetted awareness-days list on top for the social-media-specific days Google omits.

---

### Verification log (all fetched 2026-07-21)
- Google UK .ics — HTTP 200, 95,699 B, `BEGIN:VCALENDAR`, 244 VEVENT, span 2021-2031.
- Google US .ics — HTTP 200, 120,685 B, `BEGIN:VCALENDAR`, 317 VEVENT, span →2031.
- gov.uk bank-holidays.json — HTTP 200, 22,207 B, valid JSON, 3 divisions.
- Nager.Date GB 2026 — HTTP 200, 2,646 B, valid JSON.
- Nager.Date US 2026 — HTTP 200, 3,700 B, valid JSON.
